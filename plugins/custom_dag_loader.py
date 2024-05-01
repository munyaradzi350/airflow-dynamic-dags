import os
from airflow.plugins_manager import AirflowPlugin

class CustomDAGLoaderPlugin(AirflowPlugin):
    name = "custom_dag_loader"

    def __init__(self):
        self.dags_folder = os.path.join(os.path.dirname(__file__), 'dags')  # Path to the dags folder within the plugin

    def load(self):
        self._load_dags_from_folder(self.dags_folder)

    def _load_dags_from_folder(self, folder):
        for filename in os.listdir(folder):
            if filename.endswith('.py'):
                module_name = os.path.splitext(filename)[0]
                module_path = os.path.join(folder, filename)

                # Import the module as a DAG
                try:
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Check if the module defines a variable named "dag"
                    if hasattr(module, 'dag'):
                        globals()[module_name] = module.dag
                except Exception as e:
                    print(f"Error loading DAG from {module_path}: {e}")
