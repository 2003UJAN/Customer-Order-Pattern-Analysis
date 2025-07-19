import os
import streamlit as st
import matplotlib.pyplot as plt

from src.data_loader import authenticate_kaggle, download_instacart_data, load_data
from src.analysis import get_peak_order_hours, get_peak_order_days, get_top_products
from src.basket_analysis import compute_basket, get_market_basket_rules

st.set_page_config(page_title="Instacart Market Basket Analysis", layout="wide")

st.title("🛒 Instacart Market Basket Analysis Dashboard")

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# 1. Kaggle authentication
kaggle_json = st.file_uploader("Upload your Kaggle API key (kaggle.json)", type='json')

if kaggle_json:
    with open("temp_kaggle.json", "wb") as f:
        f.write(kaggle_json.getbuffer())
    authenticate_kaggle("temp_kaggle.json")
    st.success("Kaggle API key uploaded and set.")

    # 2. Download data button
    if st.button("Download Instacart Data from Kaggle"):
        with st.spinner("Downloading and extracting..."):
            download_instacart_data()
        st.success("Downloaded!")

# 3. Data availability check and load
data_files = [os.path.join(data_dir, f) for f in ["orders.csv", "products.csv", "order_products__prior.csv"]]
if all([os.path.exists(f) for f in data_files]):
    st.success("Instacart data available!")
    orders, products, order_products = load_data()

    tab1, tab2, tab3 = st.tabs(["📈 Peak Ordering Times", "🥑 Popular Items", "🤝 Bundle Patterns"])

    with tab1:
        st.header("Order Volume by Hour")
        peak_hours = get_peak_order_hours(orders)
        fig, ax = plt.subplots()
        peak_hours.plot(kind='bar', ax=ax)
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Number of Orders")
        st.pyplot(fig)

        st.header("Order Volume by Day")
        peak_days = get_peak_order_days(orders)
        fig2, ax2 = plt.subplots()
        peak_days.plot(kind='bar', ax=ax2, color='orange')
        ax2.set_xlabel("Day of Week")
        ax2.set_ylabel("Number of Orders")
        st.pyplot(fig2)

    with tab2:
        st.header("Top 20 Most Popular Products")
        top_n = st.slider("Number of top products", min_value=5, max_value=30, value=20)
        top_products = get_top_products(order_products, products, n=top_n)
        fig, ax = plt.subplots(figsize=(8,6))
        top_products.sort_values().plot(kind='barh', ax=ax)
        ax.set_xlabel("Purchase Count")
        st.pyplot(fig)

    with tab3:
        st.header("Frequently Bought Together: Bundles")
        st.write("Computing bundles on sample of 5000 orders for efficiency (can increase in code).")
        basket = compute_basket(order_products, products, n_orders=5000)
        rules = get_market_basket_rules(basket, support=0.02, min_lift=1.1)
        st.dataframe(rules.head(10))
else:
    st.info("Data not found. Please upload your `kaggle.json` and click 'Download Instacart Data from Kaggle'.")

st.markdown("---")
st.info(
    "👉 Instructions: Get your Kaggle API key from https://www.kaggle.com/settings (click 'Create New API Token').\n"
    "Upload `kaggle.json`, click download, and play!"
)
