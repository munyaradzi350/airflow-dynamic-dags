import requests
from flask import Blueprint, jsonify, current_app

airflow_controllers = Blueprint("airflow_controllers", __name__)

@airflow_controllers.route("/trigger_dag", methods=["POST"])
def trigger_dag():
    api_url = current_app.config["AIRFLOW_API_URL"]
    username = current_app.config["AIRFLOW_USERNAME"]
    password = current_app.config["AIRFLOW_PASSWORD"]

    # Example endpoint for triggering a DAG
    dag_endpoint = f"{api_url}/dags/<dag_id>/dagRuns"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "conf": {},  # Optional configuration for the DAG run
        "execution_date": "2024-05-05T00:00:00+00:00"  # Specify the execution date/time
    }

    try:
        response = requests.post(
            dag_endpoint,
            headers=headers,
            json=payload,
            auth=(username, password)
        )

        if response.status_code == 200:
            return jsonify({"message": "DAG triggered successfully!"})
        else:
            return jsonify({"error": f"Failed to trigger DAG: {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to trigger DAG: {str(e)}"}), 500
