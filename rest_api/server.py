from flask import Flask, Blueprint, jsonify, request
import requests
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Define Airflow credentials
AIRFLOW_API_URL = os.getenv("AIRFLOW_API_URL")
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD")

# Define Airflow routes blueprint
airflow_routes = Blueprint("airflow_routes", __name__)

@airflow_routes.route("/trigger_dag", methods=["POST"])
def trigger_dag():
    try:
        # Extract DAG ID from request
        dag_id = request.json["dag_id"]
        
        # Airflow API endpoint for triggering DAG runs
        dag_endpoint = f"{AIRFLOW_API_URL}/dags/{dag_id}/dagRuns"

        headers = {
            "Content-Type": "application/json"
        }

        # Payload for triggering DAG run
        payload = {
            "conf": {},  # Optional configuration for the DAG run
            "execution_date": request.json.get("execution_date") or "now"  # Default to "now" if execution_date is not provided
        }

        # Encode username and password for Basic Authentication
        auth_header = f"{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}"
        auth_header_encoded = base64.b64encode(auth_header.encode()).decode("utf-8")
        headers["Authorization"] = f"Basic {auth_header_encoded}"

        response = requests.post(
            dag_endpoint,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return jsonify({"message": "DAG triggered successfully!"}), 200
        else:
            return jsonify({"error": f"Failed to trigger DAG: {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to trigger DAG: {str(e)}"}), 500

@airflow_routes.route("/list_dags", methods=["GET"])
def list_dags():
    try:
        # Airflow API endpoint for listing all DAGs
        dag_endpoint = f"https://{AIRFLOW_API_URL}/dags/{dag_id}/dagRuns"


        headers = {
            "Content-Type": "application/json"
        }

        # Encode username and password for Basic Authentication
        auth_header = f"{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}"
        auth_header_encoded = base64.b64encode(auth_header.encode()).decode("utf-8")
        headers["Authorization"] = f"Basic {auth_header_encoded}"

        response = requests.get(
            dags_endpoint,
            headers=headers
        )

        if response.status_code == 200:
            dags_data = response.json()
            print("List of available DAGs:")
            for dag in dags_data["dags"]:
                print(f"- {dag['dag_id']}")
            return jsonify(dags_data), 200
        else:
            return jsonify({"error": f"Failed to list DAGs: {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to list DAGs: {str(e)}"}), 500

# Fetch and print list of DAGs when the application starts
try:
    dags_endpoint = f"{AIRFLOW_API_URL}/dags"

    headers = {
        "Content-Type": "application/json"
    }

    # Encode username and password for Basic Authentication
    auth_header = f"{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}"
    auth_header_encoded = base64.b64encode(auth_header.encode()).decode("utf-8")
    headers["Authorization"] = f"Basic {auth_header_encoded}"

    response = requests.get(
        dags_endpoint,
        headers=headers
    )

    if response.status_code == 200:
        dags_data = response.json()
        print("List of available DAGs:")
        for dag in dags_data["dags"]:
            print(f"- {dag['dag_id']}")
    else:
        print(f"Failed to fetch DAGs: {response.text}")
except Exception as e:
    print(f"Failed to fetch DAGs: {str(e)}")

# Register Airflow routes blueprint
app.register_blueprint(airflow_routes, url_prefix="/airflow")

if __name__ == "__main__":
    app.run(debug=True)
