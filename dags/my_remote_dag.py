from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.api.client.local_client import Client

# Define your DAG
default_args = {
    'owner': 'Munya Munya',
    'start_date': dt.datetime(2024, 4, 28),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG(
    dag_id='my_remote_dag',
    default_args=default_args,
    schedule_interval='0 * * * *',
)

# Define tasks
def print_hello():
    print('Hello!')

print_hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag,
)

# Add tasks to the DAG
print_hello_task

# Push the DAG to the remote Airflow instance
remote_airflow_url = 'http://20.164.73.163:8080/home'
client = Client(remote_airflow_url)
client.add_dag(dag)
