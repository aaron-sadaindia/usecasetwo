import variables as v
import logging
import pandas as pd
from google.cloud import bigquery
def fileValidation(**context):

    file_name=context['dag_run'].conf['name']
    uri='gs://'+v.bucket_name+'/'+file_name
    
    file_ext=file_name[-4:]
    if file_ext=='xlsx':
        ext=1
    else:
        logging.error("Table %s of different extension",file_name)
        return False
    
    dataset= pd.read_excel(uri)
    dataset.fillna(value = "NULL",inplace = True)
    if dataset.columns[0]==v.name_of_table and list(dataset.iloc[0,])==v.column_name and \
      list(dataset.iloc[1,])==v.sub_column_name :
        schema=1
    else:
        logging.error("Table %s of different schema",file_name)
        return False
    if (schema==1 and ext==1):
        return True
    return False

def ingestionToBQ(**context):
        
    """Function to ingest data into BQ"""
    file_name=context['dag_run'].conf['name']
    uri='gs://'+v.bucket_name+'/'+file_name
    dataset= pd.read_excel(uri,skiprows=[0,2])
    dataset.fillna(value = "",inplace = True)
    rows=len(dataset)
    client = bigquery.Client()
    rows_to_insert = []
    line_count=1
    
    for i in range(rows):
        try:
            _to_insert = {
                "Contributor":dataset.iloc[i,0],
                "Sub_Category":dataset.iloc[i,1],
                "Category":dataset.iloc[i,2],
                "Multiplying_Factor":int(dataset.iloc[i,3]),
                "Area_code":dataset.iloc[i,4],
                "Feature_Factors":{
                    "Feature_1":float(dataset.iloc[i,5]),
                    "Feature_2":float(dataset.iloc[i,6]),
                    "Feature_3":dataset.iloc[i,7].split(',')
                    }
                }
            line_count+=1
            rows_to_insert.append(_to_insert)
           
        except Exception as e: 
            logging.error(f"{e}-at line {line_count}-line omitted")
    try:
        client.insert_rows_json(v.table_name,rows_to_insert)
    except Exception as e:
        logging.error(f"{e}-the upload was not completed")
            
        