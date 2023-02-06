
# SustatinIT| Aaron John

Implement data pipeline for ingestion to BigQuery involving extraction, transformation, and loading of the data uploaded in
the GCS Bucket.


## Deployment

To deploy this project, the following has been pre-created 

    1. Cloud Function jobs which is triggered on creation/updation in the GCS bucket which triggers the DAGS.

    2. Functions to validate the schema and extension of the file and the function to ingest the data into the big query table

    3. Creating the infrastructure using terraform which includes the big query table, cloud composer, gcs bucket and service accounts 
    
    4. The cloud functions code, the code for the dags and the different functions and the Terraform code for the making of the infrastructure are present in the src   folder
