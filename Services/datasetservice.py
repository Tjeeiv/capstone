import os
import json
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi


def getdata():
        
        load_dotenv()

        with open ('appsetting.json') as f:
            setting = json.load(f)

        os.environ['KAGGLE_USERNAME'] = os.getenv("KaggleUsername")
        os.environ['KAGGLE_KEY'] =  os.getenv("KaggleAPIKey")

        api = KaggleApi()
        api.authenticate()
        
        api.dataset_download_files(  setting["Kaggle"]["DatasetName"] ,path=setting["Kaggle"]["DownloadPath"],unzip=True)
 
        return True