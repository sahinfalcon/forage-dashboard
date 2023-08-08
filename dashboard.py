# imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import threading
import time
from config import DATABASE_URL

# initialise dictionaries so they already exist as empty dicts
submission_count = {"count": 0}
tmins = {"datasets": []}
escs = {"datasets": []}
eeb_data = {"datasets": []}
hourly_data = {"datasets": [{"data": [], "id": "Submissions"}]}

# create flask app
app = Flask("Forage Dashboard")

# allows forage to access the data CORS = Cross-origin resource sharing
CORS(app)


# returns number of rows
def count_rows_in_responses(connection_config):
    try:
        connection = psycopg2.connect(connection_config)
        cursor = connection.cursor()
        # query to count rows in the pisa table
        cursor.execute("SELECT COUNT(*) FROM pisa;")
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count
    except (psycopg2.Error, Exception) as e:
        # so i know why its throwing an error
        print(f"Error occurred while connecting to the database: {e}")
        return 0


# calculates the learning hours per week + links to a country
def calculate_average_tmins_and_cnt(connection_config):
    try:
        connection = psycopg2.connect(connection_config)
        cursor = connection.cursor()
        # query to calculate average 'tmins' divided by 60 for each country
        cursor.execute(
            "SELECT cnt, AVG(tmins/60) FROM pisa WHERE tmins IS NOT NULL GROUP BY cnt;"
        )
        results = cursor.fetchall()
        tmins = {"datasets": []}  # to store the result
        for country, average_tmins in results:
            # convert the average tmins to a decimal with 1 decimal place
            average_tmins = (
                round(float(average_tmins), 1) if average_tmins is not None else None
            )
            # Add country and average_tmins to the tmins datasets
            tmins["datasets"].append({"country": country, "hours": average_tmins})
        cursor.close()
        connection.close()
        return tmins  # return result directly
    except (psycopg2.Error, Exception) as e:
        # so i know why its throwing an error
        print(f"Error occurred while connecting to the database: {e}")
        return None


def calculate_escs(connection_config):
    try:
        connection = psycopg2.connect(connection_config)
        cursor = connection.cursor()
        # query to select average 'escs' for each country
        cursor.execute(
            "SELECT cnt, AVG(escs) FROM pisa WHERE escs IS NOT NULL GROUP BY cnt;"
        )
        results = cursor.fetchall()
        escs_data = {"datasets": []}  # store the result
        for id, average_escs in results:
            # Convert average_escs to an decimal and round to 1dp
            average_escs = round(float(average_escs), 1)
            # add country and average_escs to the escs datasets
            escs_data["datasets"].append({"id": id, "value": average_escs})
        cursor.close()
        connection.close()
        return escs_data  # return result directly
    except (psycopg2.Error, Exception) as e:
        # so i know why its throwing an error
        print(f"Error occurred while connecting to the database: {e}")
        return None


def calculate_eeb(connection_config):
    try:
        connection = psycopg2.connect(connection_config)
        cursor = connection.cursor()
        # select 'DURECEC', 'BELONG', and count of submissions for each country
        cursor.execute(
            "SELECT cnt, AVG(durecec), AVG(belong), (COUNT(*)/5) FROM pisa WHERE durecec IS NOT NULL AND belong IS NOT NULL GROUP BY cnt;"
        )
        results = cursor.fetchall()
        eeb_data = {"datasets": []}  # store the result
        for country, durecec, belong, submissions in results:
            # convert 'durecec' to int
            durecec = int(durecec) if durecec is not None else None
            # convert 'belong' to float and round to 1 decimal place
            belong = round(float(belong), 1) if belong is not None else None
            # add country data to eeb datasets
            eeb_data["datasets"].append(
                {
                    "id": country,
                    "data": [{"x": durecec, "y": belong, "submissions": submissions}],
                }
            )
        cursor.close()
        connection.close()
        return eeb_data  # return result directly
    except (psycopg2.Error, Exception) as e:
        print(f"Error occurred while connecting to the database: {e}")
        return None


def get_entries_per_hour(source_database):
    try:
        while True:
            connection = psycopg2.connect(source_database)
            cursor = connection.cursor()
            # select number of entries per hour, order chronologically
            query = "SELECT to_char(time_submitted, 'HH24:00') AS hour, COUNT(*) AS entry_count FROM pisa GROUP BY hour ORDER BY hour;"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            # format data
            data = [{"x": entry[0], "y": entry[1]} for entry in results]
            output = {"datasets": [{"id": "Submissions", "data": data}]}
            return output
    except (psycopg2.Error, Exception) as e:
        print(f"Error occurred while connecting to the database: {e}")
        return {"datasets": []}


# refreshes once per second to allow for uptothesecond recording
def fetch_submission_count():
    while True:
        total_count = 0
        count = count_rows_in_responses(DATABASE_URL)
        total_count += count
        submission_count["count"] = total_count
        time.sleep(1)  # fetches every 1 (one) second


def fetch_tmins():
    while True:
        result = calculate_average_tmins_and_cnt(DATABASE_URL)
        if result:
            tmins["datasets"] = result["datasets"]
        time.sleep(1)  ##fetches every 1 (one) second


def fetch_escs():
    while True:
        result = calculate_escs(DATABASE_URL)
        if result:
            escs["datasets"] = result["datasets"]
        time.sleep(1)  # fetches every 1 (one) second


def fetch_eeb():
    while True:
        result = calculate_eeb(DATABASE_URL)
        if result:
            eeb_data["datasets"] = result["datasets"]
        time.sleep(1)  # fetches every 1 (one) second


def fetch_sot():
    while True:
        result = get_entries_per_hour(DATABASE_URL)
        if result:
            hourly_data["datasets"] = result["datasets"]
        time.sleep(1)  # fetches every 1 (one) second


# thread to fetch count in bg
submissions_thread = threading.Thread(target=fetch_submission_count)
submissions_thread.daemon = True
submissions_thread.start()

# thread to fetch tmins in bg
tmins_thread = threading.Thread(target=fetch_tmins)
tmins_thread.daemon = True
tmins_thread.start()

# thread to fetch escs in bg
escs_thread = threading.Thread(target=fetch_escs)
escs_thread.daemon = True
escs_thread.start()

# thread to fetch eeb in bg
eeb_thread = threading.Thread(target=fetch_eeb)
eeb_thread.daemon = True
eeb_thread.start()

# thread to fetch submissions over time in bg
sot_thread = threading.Thread(target=fetch_sot)
sot_thread.daemon = True
sot_thread.start()


# flask app routes


# total submission count route
@app.route("/submissions", methods=["GET"])
def handle_submissions():
    if request.method == "GET":
        return jsonify(submission_count)


# avg learning hours per week route
@app.route("/tmins", methods=["GET"])
def handle_tmins():
    if request.method == "GET":
        # select the diff parameters from the 'countres=' part of the get query request
        countries_param = request.args.get("countries")
        if countries_param:
            # need to split into 3 lettr country codes to correlate with 'cnt' column
            countries = countries_param.split(",")
            # filter the data based on what countries were in the query
            filtered_tmins_data = {
                "datasets": [
                    country_data
                    for country_data in escs["datasets"]
                    if country_data["id"] in countries
                ]
            }
        else:
            # get all if no specific country is selected
            filtered_tmins_data = tmins
        return jsonify(filtered_tmins_data)


# economic, social and cultural score route
@app.route("/escs", methods=["GET"])
def handle_escs():
    if request.method == "GET":
        # select the diff parameters from the 'countres=' part of the get query request
        countries_param = request.args.get("countries")
        if countries_param:
            # need to split into 3 lettr country codes to correlate with 'cnt' column
            countries = countries_param.split(",")
            # filter the data based on what countries were in the query
            filtered_escs_data = {
                "datasets": [
                    country_data
                    for country_data in escs["datasets"]
                    if country_data["id"] in countries
                ]
            }
        else:
            # get all if no specific country is selected
            filtered_escs_data = escs
        return jsonify(filtered_escs_data)


# early education and sense of belonging route
@app.route("/eeb", methods=["GET"])
def handle_eeb():
    if request.method == "GET":
        # select the diff parameters from the 'countres=' part of the get query request
        countries_param = request.args.get("countries")
        if countries_param:
            # need to split into 3 lettr country codes to correlate with 'cnt' column
            countries = countries_param.split(",")
            # filter the data based on what countries were in the query
            filtered_eeb_data = {
                "datasets": [
                    country_data
                    for country_data in eeb_data["datasets"]
                    if country_data["id"] in countries
                ]
            }
        else:
            # get all if no specific country is selected
            filtered_eeb_data = eeb_data
        return jsonify(filtered_eeb_data)


# submissions over time route
@app.route("/sot", methods=["GET"])
def handle_sot():
    if request.method == "GET":
        sot_data = get_entries_per_hour(DATABASE_URL)
        return jsonify(sot_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
