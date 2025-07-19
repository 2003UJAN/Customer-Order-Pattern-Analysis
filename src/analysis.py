import pandas as pd

def get_peak_order_hours(orders: pd.DataFrame):
    return orders['order_hour_of_day'].value_counts().sort_index()

def get_peak_order_days(orders: pd.DataFrame):
    dow_map = {0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday'}
    dow_series = orders['order_dow'].replace(dow_map)
    return dow_series.value_counts()[['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']]

def get_top_products(order_products: pd.DataFrame, products: pd.DataFrame, n=20):
    merged = order_products.merge(products, on='product_id')
    return merged['product_name'].value_counts().head(n)
