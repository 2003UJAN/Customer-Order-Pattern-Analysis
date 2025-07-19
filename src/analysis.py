import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def load_data():
    files = {
        "orders": "https://www.kaggleusercontent.com/psparks/instacart-market-basket-analysis/orders.csv",
        "order_products__prior": "https://www.kaggleusercontent.com/psparks/instacart-market-basket-analysis/order_products__prior.csv",
        "products": "https://www.kaggleusercontent.com/psparks/instacart-market-basket-analysis/products.csv",
        "departments": "https://www.kaggleusercontent.com/psparks/instacart-market-basket-analysis/departments.csv",
        "aisles": "https://www.kaggleusercontent.com/psparks/instacart-market-basket-analysis/aisles.csv"
    }

    dfs = {name: pd.read_csv(url) for name, url in files.items()}
    return dfs

def merge_data(dfs):
    merged = dfs["order_products__prior"].merge(dfs["products"], on="product_id", how="left")
    merged = merged.merge(dfs["orders"], on="order_id", how="left")
    merged = merged.merge(dfs["departments"], on="department_id", how="left")
    merged = merged.merge(dfs["aisles"], on="aisle_id", how="left")
    return merged

def generate_freq_items(merged_df):
    basket = (merged_df
              .groupby(['order_id', 'product_name'])['product_name']
              .count().unstack().reset_index().fillna(0)
              .set_index('order_id'))
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    freq_items = apriori(basket, min_support=0.02, use_colnames=True)
    return freq_items

def top_products(merged_df, n=10):
    return (merged_df['product_name'].value_counts()
            .head(n)
            .reset_index()
            .rename(columns={'index': 'product_name', 'product_name': 'count'}))

def reorder_ratio(merged_df):
    reorder_counts = merged_df.groupby('product_name')['reordered'].agg(['sum', 'count'])
    reorder_counts['reorder_ratio'] = reorder_counts['sum'] / reorder_counts['count']
    reorder_counts = reorder_counts.sort_values('reorder_ratio', ascending=False)
    return reorder_counts.head(10).reset_index()
