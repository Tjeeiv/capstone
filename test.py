import os
import shutil
from dotenv import load_dotenv

load_dotenv()

os.environ['KAGGLEHUB_CACHE'] = os.path.abspath('./rawdata')
os.environ['KAGGLE_API_TOKEN'] = os.getenv('KaggleAPIKey')

import kagglehub
cache_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
print("Downloaded to:", cache_path)

# Copy files to your clean target folder
destination = "./data"
os.makedirs(destination, exist_ok=True)

for file in os.listdir(cache_path):
    src = os.path.join(cache_path, file)
    dst = os.path.join(destination, file)
    if os.path.isfile(src):
        shutil.copy(src, dst)

print("Files copied to:", destination)
print("Files:", os.listdir(destination))