#Title: functions.py
#Description: functions.py file contains the different functions that is being carried out in the composer. The different functions 
# that it checks are 1. To check whether the extension of the file is .xlsx 2. To check whether the schema of the file uploaded is same as defined
# 3. To ingest the data into the big query 
#Pre-requisites: installing dependencies mentioned in requirements.txt

#Date           Change Name        User    
#Feb 06, 2023   Added comments     Aaron

"""Importing the required libraries and modules"""
import variables as v
import logging
import pandas as pd
from google.cloud import bigquery
def extensionCheck(**context):
    """Function to check if the extensions of the file uploaded is 
       an xlsx file 
    Arguments: Information regarding the file uploaded
    Returns:
        It returns whether the file is xlsx file or not
    """
    file_name=context['dag_run'].conf['name']
    
    file_ext=file_name[-4:]
    if file_ext=='xlsx':
        return True
    else:
        logging.error("Table %s has a different extension",file_name)
        return False
    
def schemaCheck(**context):
    """Function to check if the schema of the file uploaded is the same as
       the schema of the bigquery table
    Arguments: Information regarding the file uploaded
    Returns:
        It returns whether the file has a different schema or not 
    """
    file_name=context['dag_run'].conf['name']
    uri='gs://'+v.bucket_name+'/'+file_name
    dataset= pd.read_excel(uri)
    dataset.fillna(value = "NULL",inplace = True)
    if dataset.columns[0]==v.name_of_table and list(dataset.iloc[0,])==v.column_name and \
      list(dataset.iloc[1,])==v.sub_column_name :
        return True
    else:
        logging.error("Table %s has a different schema",file_name)
        return False


def ingestionToBQ(**context):
        
    """Function to ingest data into BQ
    Arguments: Information regarding the file uploaded
    Returns:
        The function ensures that data is ingested into the BigQuery 
    """
    file_name=context['dag_run'].conf['name']
    uri='gs://'+v.bucket_name+'/'+file_name
    dataset= pd.read_excel(uri,skiprows=[0,2])
    dataset.fillna(value = "",inplace = True)
    rows=len(dataset)
    client = bigquery.Client()
    rows_to_insert = []
    line_count=1
    
    for row in range(rows):
        try:
            _to_insert = {
                "Contributor":dataset.iloc[row,0],
                "Sub_Category":dataset.iloc[row,1],
                "Category":dataset.iloc[row,2],
                "Multiplying_Factor":int(dataset.iloc[row,3]),
                "Area_code":dataset.iloc[row,4],
                "Feature_Factors":{
                    "Feature_1":float(dataset.iloc[row,5]),
                    "Feature_2":float(dataset.iloc[row,6]),
                    "Feature_3":dataset.iloc[row,7].split(',')
                    }
                }
            line_count+=1
            rows_to_insert.append(_to_insert)
           
        except Exception as errorInRows: 
            logging.error(f"{errorInRows}-at line {line_count}-line omitted")
    try:
        client.insert_rows_json(v.table_name,rows_to_insert)
    except Exception as incompleteUpload:
        logging.error(f"{incompleteUpload}-the upload was not completed")
            
        