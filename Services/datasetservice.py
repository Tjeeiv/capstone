import os
import shutil
import json
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
import kagglehub
import snowflake.connector

def getdata():
        
        load_dotenv()
        os.environ['KAGGLEHUB_CACHE'] = os.path.abspath('./rawdata')
        os.environ['KAGGLE_API_TOKEN'] = os.getenv('KaggleAPIKey')
        cache_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
        
        conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
            )
        cs = conn.cursor()
        UploadedFiles = []
        try:
              for file in os.listdir(cache_path):
                     file = os.path.join(cache_path,file)

                     if os.path.isfile(file):
                            filepath = file.replace("\\","/")
                            putcommand = f"PUT 'file://{filepath}' @CAPSTONERAWDATAFILES  AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
                            cs.execute(putcommand)

                            filename = os.path.basename(filepath)
                            UploadedFiles.append(filename)
          
        finally:
               cs.close()
               conn.close()
                
        shutil.rmtree('./rawdata', ignore_errors=True)
        return UploadedFiles
 
  