import pandas as pd
import os
from mlxtend.frequent_patterns import apriori, association_rules

def load_data():
    base_path = "data"
    files = {
        "orders": os.path.join(base_path, "orders.csv"),
        "products": os.path.join(base_path, "products.csv"),
        "order_products": os.path.join(base_path, "order_products__prior.csv"),
        "departments": os.path.join(base_path, "departments.csv"),
        "aisles": os.path.join(base_path, "aisles.csv")
    }

    dfs = {}
    for name, path in files.items():
        dfs[name] = pd.read_csv(path)
    return dfs

def merge_data(dfs):
    data = dfs["order_products"].merge(dfs["orders"], on="order_id") \
                                 .merge(dfs["products"], on="product_id") \
                                 .merge(dfs["departments"], on="department_id") \
                                 .merge(dfs["aisles"], on="aisle_id")
    return data

def reorder_ratio(data):
    return data.groupby("product_name")["reordered"].mean().sort_values(ascending=False)

def top_products(data, n=10):
    return data["product_name"].value_counts().head(n)

def generate_freq_items(data, min_support=0.01):
    basket = data[data['eval_set'] == 'prior'].groupby(['order_id', 'product_name'])['reordered'].count().unstack().fillna(0)
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)

    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    return frequent_itemsets, rules
