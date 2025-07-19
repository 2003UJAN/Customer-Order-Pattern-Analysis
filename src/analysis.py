import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# Set Kaggle API credentials path
os.environ['KAGGLE_CONFIG_DIR'] = os.path.join(os.getcwd(), '.kaggle')

# Authenticate and download files
def download_data():
    api = KaggleApi()
    api.authenticate()
    dataset = 'psparks/instacart-market-basket-analysis'
    files = ['aisles.csv', 'departments.csv', 'products.csv', 'orders.csv', 'order_products__prior.csv', 'order_products__train.csv']

    for file in files:
        print(f"Downloading {file}...")
        api.dataset_download_file(dataset, file_name=file, path='data', force=True)

        # Unzip the downloaded file
        zipped_path = os.path.join('data', f"{file}.zip")
        if os.path.exists(zipped_path):
            import zipfile
            with zipfile.ZipFile(zipped_path, 'r') as zip_ref:
                zip_ref.extractall('data')
            os.remove(zipped_path)

def load_data():
    orders = pd.read_csv('data/orders.csv')
    products = pd.read_csv('data/products.csv')
    departments = pd.read_csv('data/departments.csv')
    aisles = pd.read_csv('data/aisles.csv')
    prior = pd.read_csv('data/order_products__prior.csv')
    train = pd.read_csv('data/order_products__train.csv')
    return orders, products, departments, aisles, prior, train

def analyze_data():
    orders, products, departments, aisles, prior, train = load_data()
    # Example: top 10 reordered products
    top_products = prior.merge(products, on='product_id') \
                        .groupby('product_name') \
                        .size() \
                        .sort_values(ascending=False) \
                        .head(10)
    return top_products
