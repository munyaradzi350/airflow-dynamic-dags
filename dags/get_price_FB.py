from airflow import DAG
from airflow.decorators import task
from datetime import datetime


with DAG("get_price_FB", start_date=datetime(2024, 4, 30), schedule_interval="@daily",
         catchup=False) as dag:
      

    @task
    def extract(stock):
        return stock

    @task
    def process(stock):
        return stock

    @task
    def send_email(stock):
        print(stock)
        return stock

    send_email(process(extract(220)))