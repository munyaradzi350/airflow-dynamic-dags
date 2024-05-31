from datetime import timedelta
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
import requests

import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the actual implementation of get_fresh_token from your scripts.token_retrieval module
from scripts.token_retrieval import get_fresh_token

default_args = {
    'owner': 'munyah',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

def retrieve_token():
    try:
        token = get_fresh_token()  
        print(f"Retrieved Token: {token}")
        return token
    except Exception as e:
        print(f"Error retrieving token: {e}")
        raise

def print_headers(token):
    if not token:
        print("Token not found")
    else:
        headers = {"Authorization": f"Bearer {token}"}
        print(f"Headers: {headers}")

def call_api(token):
    print(f"Token before API call: {token}")  
    
    # Get the connection details that you set in airflow environment
    conn = BaseHook.get_connection('eezimeds_patients')
    endpoint = '/mongo/patient'  
    url = f"{conn.host}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response json: {response.json}")
        
        # Handle token expiration and refresh if needed
        if response.status_code == 401: 
            print("Token expired. Refreshing...")
            token = get_fresh_token()  # Refresh the token
            headers["Authorization"] = f"Bearer {token}"  
            response = requests.get(url, headers=headers)  # Make the API call again
            
            # Check the response after token refresh
            if response.status_code == 200:
                patient_data = response.json()
                print(f"patient data: {patient_data}")
            else:
                print(f"Failed to retrieve patient after token refresh. Status code: {response.status_code}")
        elif response.status_code == 200:
            patient_data = response.json()  
            print(f"patient data: {patient_data}")
        else:
            print(f"Failed to retrieve patient. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error during API call: {e}")

with DAG(
    'patients_api_dag',
    default_args=default_args,
    description='A DAG to retrieve patient data from the eezimeds API',
    schedule_interval=timedelta(minutes=5),
    start_date=pendulum.today('UTC').add(days=-1),
    catchup=False,
) as dag:

    retrieve_token_task = PythonOperator(
        task_id='retrieve_token',
        python_callable=retrieve_token,
    )

    debug_headers_task = PythonOperator(
        task_id='debug_headers',
        python_callable=print_headers,
        op_args=[retrieve_token_task.output],  
    )

    retrieve_patient_task = PythonOperator(
        task_id='retrieve_patients',
        python_callable=call_api,
        op_args=[retrieve_token_task.output],  
    )

    retrieve_token_task >> debug_headers_task >> retrieve_patient_task