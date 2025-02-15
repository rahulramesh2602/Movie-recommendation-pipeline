from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


def upload_to_s3():
    from Scripts.upload_to_s3 import upload_to_s3 as upload

    upload()


# Define the DAG
dag = DAG(
    "movie_recommendation_pipeline",
    description="A pipeline to process movie data and generate recommendations",
    schedule_interval="@daily",  # Run daily
    start_date=datetime(2023, 10, 1),
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
