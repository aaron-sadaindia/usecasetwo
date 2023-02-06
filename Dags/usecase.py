#Title: usecase.py
#Description: usecase.py file contains the dag compose_sample_trigger_response_dag and the tasks are carried out like the filevalidation, schema check and 
#Bigquery ingestion 
#Pre-requisites: installing dependencies mentioned in requirements.txt
#Triggered by cloud function named triggered
#Date           Change Name        User    
#Feb 06, 2023   Added comments     Aaron


"""Importing the required libraries and modules"""
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import ShortCircuitOperator
from functions import extensionCheck
from functions import schemaCheck
from functions import ingestionToBQ
import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


with DAG("Storage_trigger_response_dag",start_date=datetime(2021, 1 ,1),
 schedule_interval=None,catchup=False) as dag:

    task_model_A = ShortCircuitOperator(
        
        task_id='fileValidation',
        python_callable=extensionCheck
        )
    task_model_B = ShortCircuitOperator(
        
        task_id='Schema_Check',
        python_callable=schemaCheck
        )
    task_model_C = PythonOperator(

            task_id="Biqquery_ingestion",
            python_callable=ingestionToBQ
        )
    task_model_A>>task_model_B>>task_model_C