import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AIRFLOW_API_URL = os.getenv('AIRFLOW_API_URL')
    AIRFLOW_USERNAME = os.getenv('AIRFLOW_USERNAME')
    AIRFLOW_PASSWORD = os.getenv('AIRFLOW_PASSWORD')
