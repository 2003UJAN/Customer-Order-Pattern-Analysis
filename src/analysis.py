import pandas as pd
import os

DATA_DIR = "data"

def load_data():
    """
    Loads required CSV files from the data directory.

    Returns:
        orders: DataFrame
        order_products: DataFrame
        products: DataFrame
    Raises:
        FileNotFoundError: if any required file is missing
    """
    required_files = [
        "orders.csv",
        "order_products__prior.csv",
        "products.csv"
    ]

    # Check if all files exist
    missing = [f for f in required_files if not os.path.exists(os.path.join(DATA_DIR, f))]
    if missing:
        raise FileNotFoundError(
            f"Missing files: {', '.join(missing)}. "
            f"Please download them from https://www.kaggle.com/datasets/instacart/market-basket-analysis "
            f"and place them in the 'data/' folder."
        )

    # Load datasets
    orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
    order_products = pd.read_csv(os.path.join(DATA_DIR, "order_products__prior.csv"))
    products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))

    return orders, order_products, products


def get_peak_order_hours(orders):
    return orders['order_hour_of_day'].value_counts().sort_index()


def get_popular_products(order_products, products, orders, start_hour=0, end_hour=23):
    # Merge all data
    merged = pd.merge(order_products, products, on='product_id')
    order_info = pd.merge(orders, merged, on='order_id')

    # Filter by hour
    filtered = order_info[
        (order_info['order_hour_of_day'] >= start_hour) &
        (order_info['order_hour_of_day'] <= end_hour)
    ]

    return filtered['product_name'].value_counts().head(10)


def get_bundle_size_distribution(order_products):
    return order_products.groupby("order_id").size()


