import os
import pandas as pd
import streamlit as st
import altair as alt

# File paths
data_dir = "data"
file_paths = {
    "orders.csv": os.path.join(data_dir, "orders.csv"),
    "products.csv": os.path.join(data_dir, "products.csv"),
    "order_products__prior.csv": os.path.join(data_dir, "order_products__prior.csv"),
    "order_products__train.csv": os.path.join(data_dir, "order_products__train.csv"),
    "aisles.csv": os.path.join(data_dir, "aisles.csv"),
    "departments.csv": os.path.join(data_dir, "departments.csv"),
}

# Kaggle links
file_links = {
    "orders.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=orders.csv",
    "products.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=products.csv",
    "order_products__prior.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=order_products__prior.csv",
    "order_products__train.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=order_products__train.csv",
    "aisles.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=aisles.csv",
    "departments.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=departments.csv",
}

# Check for missing files
missing = [f for f, path in file_paths.items() if not os.path.exists(path)]

if missing:
    st.error("❌ Missing required data files.")
    for f in missing:
        st.markdown(f"- [{f}]({file_links[f]})")
    st.markdown("👉 Please place them in the `data/` directory and reload.")
    st.stop()

# Load datasets
orders = pd.read_csv(file_paths["orders.csv"])
products = pd.read_csv(file_paths["products.csv"])
prior = pd.read_csv(file_paths["order_products__prior.csv"])
train = pd.read_csv(file_paths["order_products__train.csv"])
aisles = pd.read_csv(file_paths["aisles.csv"])
departments = pd.read_csv(file_paths["departments.csv"])

# Streamlit App
st.title("🛒 Instacart Basket Analysis Dashboard")

# Top ordered products
st.subheader("Top 10 Most Ordered Products")
top_products = (
    prior.groupby("product_id")
    .size()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="order_count")
    .merge(products, on="product_id")
)

chart = (
    alt.Chart(top_products)
    .mark_bar()
    .encode(
        x=alt.X("order_count:Q", title="Order Count"),
        y=alt.Y("product_name:N", sort="-x", title="Product"),
        tooltip=["product_name", "order_count"]
    )
    .properties(height=400)
)
st.altair_chart(chart, use_container_width=True)

# Aisle analysis
st.subheader("Top 5 Aisles by Order Volume")
aisle_counts = (
    prior.merge(products, on="product_id")
         .merge(aisles, on="aisle_id")
         .groupby("aisle")["order_id"]
         .count()
         .sort_values(ascending=False)
         .head(5)
         .reset_index(name="order_count")
)

st.bar_chart(data=aisle_counts.set_index("aisle"))
