from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import ShortCircuitOperator
from functions import fileValidation
from functions import ingestionToBQ
import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


with DAG("composer_sample_trigger_response_dag",start_date=datetime(2021, 1 ,1),
 schedule_interval=None,catchup=False) as dag:

    task_model_A = ShortCircuitOperator(
        task_id='fileValidation',
        python_callable=fileValidation
        )
    task_model_B = PythonOperator(

            task_id="Biqquery_ingestion",
            python_callable=ingestionToBQ
        )
    task_model_A>>task_model_B