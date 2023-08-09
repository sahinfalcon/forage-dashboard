# imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from config import DATABASE_URL
from collections import defaultdict 

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
            "SELECT cnt, AVG(tmins/60) FROM pisa WHERE tmins IS NOT NULL GROUP BY cnt ORDER BY cnt;"
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
            "SELECT cnt, AVG(durecec), AVG(belong), (COUNT(*)) FROM pisa WHERE durecec IS NOT NULL AND belong IS NOT NULL GROUP BY cnt;"
        )
        results = cursor.fetchall()
        eeb_data = {"datasets": []}  # store the result
        for country, durecec, belong, submissions in results:
            # convert 'durecec' to float
            durecec = round(float(durecec), 1) if durecec is not None else None
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


def get_entries_per_hour(connection_config):
    try:
        connection = psycopg2.connect(connection_config)
        cursor = connection.cursor()
        # Query to select the hour timestamp and count of submissions for each hour
        cursor.execute("SELECT DATE_TRUNC('hour', timestamp) as x, COUNT(*) as y FROM pisa GROUP BY x;")
        results = cursor.fetchall()
        # Create a defaultdict to store the data
        minute_wise_data = defaultdict(int)
        # Populate the defaultdict with the hour timestamp and count of submissions
        for timestamp, count in results:
            formatted_timestamp = timestamp.strftime("%H:%M")
            minute_wise_data[formatted_timestamp] = count
        cursor.close()
        connection.close()
        # Sort the data based on the timestamp (x) values
        sorted_data = sorted(minute_wise_data.items(), key=lambda item: item[0])
        # Create the final dataset in the required format
        dataset = {
            "id": "Submissions",
            "data": [{"x": timestamp, "y": count} for timestamp, count in sorted_data]
        }
        return {"datasets": [dataset]}
    except (psycopg2.Error, Exception) as e:
        print(f"Error occurred while connecting to the database: {e}")
        return {"datasets": []} 


# refreshes once per second to allow for uptothesecond recording
def fetch_submission_count():
    count = count_rows_in_responses(DATABASE_URL)
    submission_count["count"] = count


def fetch_tmins():
    result = calculate_average_tmins_and_cnt(DATABASE_URL)
    if result:
        tmins["datasets"] = result["datasets"]


def fetch_escs():
    result = calculate_escs(DATABASE_URL)
    if result:
        escs["datasets"] = result["datasets"]


def fetch_eeb():
    result = calculate_eeb(DATABASE_URL)
    if result:
        eeb_data["datasets"] = result["datasets"]


def fetch_sot():
    result = get_entries_per_hour(DATABASE_URL)
    if result:
        hourly_data["datasets"] = result["datasets"]


# function to configure dashboard menu which filters graph by country
def filter_by_country_menu(metric):
    # select the diff parameters from the 'countries' part of the get query request
    countries_param = request.args.get("countries")
    if countries_param:
        # need to split into 3 letter country codes to correlate with 'cnt' column
        countries = countries_param.split(",")
        # filter the data based on what countries were in the query
        filtered_data = {
            "datasets": [
                country_data
                for country_data in metric["datasets"]
                if country_data["country" if metric == tmins else "id"] in countries
            ]
        }
    else:
        # get all if no specific country is selected
        filtered_data = metric
    return filtered_data


# total submission count route
@app.route("/submissions", methods=["GET"])
def handle_submissions():
    if request.method == "GET":
        fetch_submission_count()
        return jsonify(submission_count)


# avg learning hours per week route
@app.route("/tmins", methods=["GET"])
def handle_tmins():
    if request.method == "GET":
        fetch_tmins()
        filtered_tmins_data = filter_by_country_menu(tmins)
        return jsonify(filtered_tmins_data)


# economic, social and cultural score route
@app.route("/escs", methods=["GET"])
def handle_escs():
    if request.method == "GET":
        fetch_escs()
        filtered_escs_data = filter_by_country_menu(escs)
        return jsonify(filtered_escs_data)


# early education and sense of belonging route
@app.route("/eeb", methods=["GET"])
def handle_eeb():
    if request.method == "GET":
        fetch_eeb()
        filtered_eeb_data = filter_by_country_menu(eeb_data)
        return jsonify(filtered_eeb_data)


# submissions over time route
@app.route("/sot", methods=["GET"])
def handle_sot():
    if request.method == "GET":
        fetch_sot()
        return jsonify(hourly_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
