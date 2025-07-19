import os
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import streamlit as st

@st.cache_data
def load_data():
    base_url = "https://www.kaggleusercontent.com/datasets/psparks/instacart-market-basket-analysis/data?select="
    
    files = {
        "orders": "orders.csv",
        "products": "products.csv",
        "order_products_prior": "order_products__prior.csv",
        "order_products_train": "order_products__train.csv",
        "aisles": "aisles.csv",
        "departments": "departments.csv"
    }

    dataframes = {}
    for key, file in files.items():
        try:
            df = pd.read_csv(f"{base_url}{file}")
            dataframes[key] = df
        except Exception as e:
            st.error(f"Failed to load {file}: {e}")
            dataframes[key] = pd.DataFrame()

    return dataframes


def merge_data(data):
    orders = data["orders"]
    prior = data["order_products_prior"]
    products = data["products"]
    aisles = data["aisles"]
    departments = data["departments"]

    merged = prior.merge(products, on='product_id', how='left') \
                  .merge(orders, on='order_id', how='left') \
                  .merge(aisles, on='aisle_id', how='left') \
                  .merge(departments, on='department_id', how='left')
    return merged


def generate_freq_items(merged_data, min_support=0.01):
    basket = merged_data.groupby(['order_id', 'product_name'])['add_to_cart_order'].count().unstack().fillna(0)
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)

    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    return frequent_itemsets, rules


def top_products(merged_data, n=10):
    return merged_data['product_name'].value_counts().head(n)


def reorder_ratio(merged_data):
    return merged_data.groupby('product_name')['reordered'].mean().sort_values(ascending=False).head(10)
