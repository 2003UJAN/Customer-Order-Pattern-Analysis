import pandas as pd
import os

DATA_PATH = "data"

REQUIRED_FILES = [
    "orders.csv",
    "order_products__prior.csv",
    "products.csv"
]

KAGGLE_LINKS = {
    "orders.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=orders.csv",
    "order_products__prior.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=order_products__prior.csv",
    "products.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=products.csv"
}

def check_files_exist():
    missing = [f for f in REQUIRED_FILES if not os.path.exists(os.path.join(DATA_PATH, f))]
    return missing

def show_missing_file_message(missing_files):
    print("\nMissing data files. Please download them from the links below and place in the `data/` folder:\n")
    for file in missing_files:
        print(f"- {file}: {KAGGLE_LINKS[file]}")

def load_data():
    missing_files = check_files_exist()
    if missing_files:
        raise FileNotFoundError(
            f"Missing files: {', '.join(missing_files)}.\n"
            f"Please download them from Kaggle and place them in the 'data/' folder.\n\n"
            + "\n".join([f"{f}: {KAGGLE_LINKS[f]}" for f in missing_files])
        )

    orders = pd.read_csv(os.path.join(DATA_PATH, "orders.csv"))
    order_products = pd.read_csv(os.path.join(DATA_PATH, "order_products__prior.csv"))
    products = pd.read_csv(os.path.join(DATA_PATH, "products.csv"))
    return orders, order_products, products

def get_peak_order_hours(orders):
    return orders['order_hour_of_day'].value_counts().sort_index()

def get_popular_products(order_products, products, orders, start_hour, end_hour):
    merged = order_products.merge(orders, on="order_id").merge(products, on="product_id")
    time_filtered = merged[(merged['order_hour_of_day'] >= start_hour) & (merged['order_hour_of_day'] <= end_hour)]
    top_products = time_filtered['product_name'].value_counts().head(10)
    return top_products

def get_bundle_size_distribution(order_products):
    return order_products.groupby("order_id")["product_id"].count()
