import os
import shutil
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
import kagglehub 
from snowflakeconnector import get_snowflake_connection

def getdata( ):
        
        load_dotenv()
        os.environ['KAGGLEHUB_CACHE'] = os.path.abspath('./rawdata')
        os.environ['KAGGLE_API_TOKEN'] = os.getenv('KaggleAPIKey')
        cache_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
        
        conn = get_snowflake_connection()
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

 