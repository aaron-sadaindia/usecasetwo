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

    task_model_A = ShortCircuitOperator(               # this short circuit operator will skip the next task if the value returned is false which in this case will be  if the file has a wrong extension
                                        
        task_id='fileValidation',
        python_callable=extensionCheck
        )
    task_model_B = ShortCircuitOperator(                # this short circuit operator will skip the next task if the value returned is false which in this case will be  if the file has the wrong schema
        
        task_id='Schema_Check',
        python_callable=schemaCheck
        )
    task_model_C = PythonOperator(                     # This python operator helps to ingest the data into the bigquery

            task_id="Biqquery_ingestion",
            python_callable=ingestionToBQ
        )
    task_model_A>>task_model_B>>task_model_C