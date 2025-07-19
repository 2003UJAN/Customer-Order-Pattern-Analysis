import os
import pandas as pd
import shutil

def authenticate_kaggle(kaggle_json_path):
    kaggle_dir = os.path.expanduser("~/.kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)
    shutil.copy(kaggle_json_path, os.path.join(kaggle_dir, "kaggle.json"))
    os.chmod(os.path.join(kaggle_dir, "kaggle.json"), 0o600)

def download_instacart_data():
    from kaggle.api.kaggle_api_extended import KaggleApi
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    dataset = "psparks/instacart-market-basket-analysis"
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=data_dir, unzip=True)

def load_data(data_dir="data"):
    orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    products = pd.read_csv(os.path.join(data_dir, "products.csv"))
    order_products = pd.read_csv(os.path.join(data_dir, "order_products__prior.csv"))
    return orders, products, order_products
