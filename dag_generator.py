import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Define the list of DAG parameters
dags = [
    {'dag_id': 'get_price_APPL', 'start_date': datetime(2024, 4, 30), 'schedule_interval': '@weekly', 'catchup': False, 'input_value': 3324},
    {'dag_id': 'get_price_FB', 'start_date': datetime(2024, 4, 30), 'schedule_interval': '@daily', 'catchup': False, 'input_value': 220},
    {'dag_id': 'get_price_GOOGL', 'start_date': datetime(2024, 4, 30), 'schedule_interval': '@daily', 'catchup': False, 'input_value': 126}
]

# Initialize Jinja2 environment
file_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(file_dir))
template = env.get_template('dag_template.jinja2')

# Generate and write DAGs to separate files
for dag_params in dags:
    dag_id = dag_params['dag_id']
    start_date = dag_params['start_date']
    schedule_interval = dag_params['schedule_interval']
    catchup = dag_params['catchup']
    input_value = dag_params['input_value']

    # Render the DAG template with the specific parameters
    dag_code = template.render(start_date=start_date, schedule_interval=schedule_interval,
                               dag_id=dag_id, catchup=catchup, input_value=input_value)
    
    # Write the generated DAG code to a Python file in the DAGs folder
    dag_file_path = os.path.join(file_dir, 'dags', f'{dag_id}.py')
    with open(dag_file_path, 'w') as f:
        f.write(dag_code)

    print(f"DAG {dag_id} successfully generated and written to {dag_file_path}")
