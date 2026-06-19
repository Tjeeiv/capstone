import os
import json
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
import kagglehub


load_dotenv()

with open ('appsetting.json') as f:
    setting = json.load(f)

os.environ['KAGGLE_USERNAME'] = "tjeeiv"
os.environ['KAGGLE_KEY'] =  "KGAT_d3b43b466a39d0acb1d036864e79a166"

api = KaggleApi()
api.authenticate()
        
# api.dataset_download_files(  setting["Kaggle"]["DatasetName"] ,path=setting["Kaggle"]["DownloadPath"],unzip=True)
 
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

print("Path to dataset files:", path)

 #KGAT_d3b43b466a39d0acb1d036864e79a166