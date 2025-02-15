from airflow import DAG
from airflow.operators.python_operator import PythonOperator  # type: ignore
from datetime import datetime
import sys
import os

# Import functions from the Scripts module
from upload_to_s3 import upload_to_s3  # type: ignore
from preprocess_data import preprocess_data  # type: ignore

# Ensure the Scripts directory is in the Python module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Scripts")))

# Define the DAG
dag = DAG(
    "movie_recommendation_pipeline",
    description="A pipeline to process movie data and generate recommendations",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)

# Task 1: Upload data to S3
upload_task = PythonOperator(
    task_id="upload_to_s3",
    python_callable=upload_to_s3,
    dag=dag,
)

# Task 2: Preprocess data
preprocess_task = PythonOperator(
    task_id="preprocess_data",
    python_callable=preprocess_data,
    dag=dag,
)

# Define task dependencies
upload_task >> preprocess_task
