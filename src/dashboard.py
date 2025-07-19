import streamlit as st
from analysis import load_data, get_peak_order_hours, get_popular_products, get_bundle_size_distribution
import matplotlib.pyplot as plt

st.set_page_config(page_title="Instacart Order Insights", layout="wide")

st.title("🛒 E-Commerce-Customer-Order-Pattern-Analysis Dashboard")

try:
    orders, order_products, products = load_data()
    st.success("Data loaded successfully!")

    st.subheader("🕒 Peak Order Hours")
    peak_hours = get_peak_order_hours(orders)
    st.bar_chart(peak_hours)

    st.subheader("🔥 Top Products Ordered (By Hour Range)")
    col1, col2 = st.columns(2)
    with col1:
        start_hour = st.slider("Start Hour", 0, 23, 8)
    with col2:
        end_hour = st.slider("End Hour", 0, 23, 17)

    top_products = get_popular_products(order_products, products, orders, start_hour, end_hour)
    st.dataframe(top_products.reset_index().rename(columns={'index': 'Product', 'product_name': 'Order Count'}))

    st.subheader("📦 Bundle Size Distribution (Items per Order)")
    bundle_sizes = get_bundle_size_distribution(order_products)
    fig, ax = plt.subplots()
    bundle_sizes.hist(bins=30, ax=ax)
    st.pyplot(fig)

except FileNotFoundError as e:
    st.error(str(e))
