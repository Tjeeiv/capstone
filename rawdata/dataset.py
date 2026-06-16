import os
os.environ['KAGGLE_USERNAME'] = 'tjeeiv'
os.environ['KAGGLE_KEY'] = 'KGAT_2b4effa289abf2f6d5a3fb99fde9426f'

import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

api.dataset_download_files(
    'olistbr/brazilian-ecommerce',
    path='./data',
    unzip=True
) 
# KGAT_2b4effa289abf2f6d5a3fb99fde9426f


