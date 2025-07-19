import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import load_data

st.set_page_config(page_title="Customer Order Pattern Analysis", layout="wide")

st.title("📊 E-Commerce Customer Order Pattern Analysis")

# Try loading data
try:
    orders, order_products, products = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# Merge product names into ordered data
merged = pd.merge(order_products, products, on='product_id')
order_info = pd.merge(orders, merged, on='order_id')

# Sidebar filters
st.sidebar.title("Filters")
selected_hour = st.sidebar.slider("Select Order Hour of Day", 0, 23, (0, 23))

# Filter by hour
filtered = order_info[
    (order_info['order_hour_of_day'] >= selected_hour[0]) &
    (order_info['order_hour_of_day'] <= selected_hour[1])
]

# Plot 1: Peak Order Times
st.subheader("⏰ Peak Order Hours")
order_hour_counts = orders['order_hour_of_day'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.plot(order_hour_counts.index, order_hour_counts.values, marker='o')
ax1.set_xlabel("Hour of Day")
ax1.set_ylabel("Order Count")
st.pyplot(fig1)

# Plot 2: Popular Products
st.subheader("🥑 Most Ordered Products (Filtered by Hour)")
top_products = (
    filtered['product_name']
    .value_counts()
    .head(10)
)
st.bar_chart(top_products)

# Plot 3: Bundle Patterns
st.subheader("🧺 Bundle Size Distribution")
bundle_size = order_products.groupby("order_id").size()
fig2, ax2 = plt.subplots()
ax2.hist(bundle_size, bins=30, color="orange", edgecolor="black")
ax2.set_xlabel("Number of Items per Order")
ax2.set_ylabel("Number of Orders")
st.pyplot(fig2)

st.markdown("---")
st.markdown("Made with ❤️ for Blinkit Internship")
