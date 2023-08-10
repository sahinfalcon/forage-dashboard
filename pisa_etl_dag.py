from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
import logging
import pandas as pd

# List of country codes to process
country_codes = [
    "alb",
    "arg",
    "aus",
    "aut",
    "bel",
    "bgr",
    "bih",
    "blr",
    "bra",
    "brn",
    "can",
    "che",
    "chl",
    "col",
    "cri",
    "cze",
    "deu",
    "dnk",
    "dom",
    "esp",
]


# Task to fetch the offset for each country from analytical_db_rds
def get_offset():
    # Connect to analytical_db_rds
    src_db = PostgresHook(postgres_conn_id="analytical_db_rds")
    src_conn = src_db.get_conn()

    # For each country code, fetch and set the submission count
    for country_code in country_codes:
        try:
            df = pd.read_sql(
                f""" 
                SELECT COUNT(*)
                FROM pisa
                WHERE cnt = '{country_code.upper()}';
                """,
                src_conn,
            )
            count = int(df["count"])
        except Exception as e:
            count = 0
            logging.info(f"Reason for failure: {e}")

        # Set the submission count as a Variable
        Variable.set(f"{country_code}_count", count)
    src_conn.close()


# Task to extract data from source databases and push to Xcom
def extract(**kwargs):
    for country_code in country_codes:
        src_db = PostgresHook(postgres_conn_id=f"seta-{country_code}")
        src_conn = src_db.get_conn()
        count = Variable.get(f"{country_code}_count")

        # Fetch data from responses table with an offset
        df = pd.read_sql(
            f"""
            SELECT id, cnt, escs, tmins, belong, durecec
            FROM responses
            OFFSET {count};
            """,
            src_conn,
        )

        # Push the extracted data to Xcom for later use
        kwargs["ti"].xcom_push(key=country_code, value=df.to_json())
        logging.info(f"Extract function: pushing dataset to Xcom")
    src_conn.close()


# Task to load data into analytical_db_rds
def load(**kwargs):
    target_db = PostgresHook(postgres_conn_id="analytical_db_rds")

    # Create the pisa table if not exists with a composite primary key
    create_posts_table = """
    CREATE TABLE IF NOT EXISTS pisa (
    id INT,
    cnt TEXT,
    escs NUMERIC(15, 4),
    tmins INT,
    belong NUMERIC(15, 4),
    durecec INT,
    time_submitted TIMESTAMP,
    PRIMARY KEY (id, cnt)
    );
    """

    # SQL query to insert data into pisa table with conflict handling
    load_post_data = """
    INSERT INTO pisa (id, cnt, escs, tmins, belong, durecec, time_submitted)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id, cnt) DO NOTHING;
    """

    for country_code in country_codes:
        df = pd.read_json(kwargs["ti"].xcom_pull(key=country_code))
        logging.info(
            f"Load function: pulled dataset from Xcom. DataFrame shape is {df.shape}"
        )

        columns = ["id", "cnt", "escs", "tmins", "belong", "durecec"]

        df = df[columns]
        df["time_submitted"] = datetime.now()

        # Change 'NA' values to None
        for column in columns:
            df[column] = df[column].replace("NA", None)

        # Load data into analytical_db_rds
        with target_db.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_posts_table)
                for row in df.itertuples():
                    data = row[1:]
                    logging.info(f"Loading data: {data}")
                    cursor.execute(load_post_data, data)
                conn.commit()
    conn.close()


# Define the DAG
dag = DAG(
    "pisa_dag",
    description="Extracts data from seta databases and moves to analytical db",
    schedule_interval=timedelta(seconds=30),
    start_date=datetime(2023, 8, 2),
    catchup=False,
    max_active_runs=1,
    tags=["PISA"],
)

# Define tasks
get_offset_task = PythonOperator(
    task_id="get_offset_task", python_callable=get_offset, provide_context=True, dag=dag
)

extract_task = PythonOperator(
    task_id="extract_task", python_callable=extract, provide_context=True, dag=dag
)

loading_task = PythonOperator(
    task_id="load_to_analytical_db", python_callable=load, provide_context=True, dag=dag
)

# Set task dependencies
get_offset_task >> extract_task >> loading_task
