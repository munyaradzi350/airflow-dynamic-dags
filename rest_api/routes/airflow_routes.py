from flask import Blueprint
from controllers.airflow_controllers import airflow_controllers

airflow_routes = Blueprint("airflow_routes", __name__)

airflow_routes.register_blueprint(airflow_controllers)
