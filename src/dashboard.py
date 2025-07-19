import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import download_data, load_data

st.set_page_config(page_title="E-Commerce Order Pattern Dashboard", layout="wide")
sns.set(style="whitegrid")

# Title
st.title("🛒 E-Commerce Customer Order Pattern Dashboard")

# Button to download data
if st.button("🔽 Download Instacart Data"):
    with st.spinner("Downloading data..."):
        download_data()
    st.success("Data downloaded!")

# Load data
orders, products, departments, aisles, prior, train = load_data()

# Merge product info
products_full = products.merge(aisles, on='aisle_id').merge(departments, on='department_id')

# Merge prior orders with product info
prior_full = prior.merge(products_full, on='product_id').merge(orders, on='order_id')

st.header("📌 Key Insights")

# 1. Top 10 reordered products
st.subheader("🔁 Top 10 Reordered Products")
top_reordered = prior_full['product_name'].value_counts().head(10)
fig1, ax1 = plt.subplots()
sns.barplot(y=top_reordered.index, x=top_reordered.values, ax=ax1, palette='viridis')
ax1.set_xlabel("Reorder Count")
ax1.set_ylabel("Product Name")
st.pyplot(fig1)

# 2. Orders by Day of Week
st.subheader("📅 Orders by Day of Week")
dow_map = {
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday',
    3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'
}
orders['order_dow_label'] = orders['order_dow'].map(dow_map)
dow_counts = orders['order_dow_label'].value_counts().reindex(dow_map.values())
fig2, ax2 = plt.subplots()
sns.barplot(x=dow_counts.index, y=dow_counts.values, ax=ax2, palette='coolwarm')
ax2.set_xlabel("Day of Week")
ax2.set_ylabel("Number of Orders")
ax2.set_title("Orders Distribution by Weekday")
st.pyplot(fig2)

# 3. Orders by Hour of Day
st.subheader("🕒 Orders by Hour of Day")
fig3, ax3 = plt.subplots()
sns.histplot(orders['order_hour_of_day'], bins=24, kde=False, ax=ax3, color='skyblue')
ax3.set_xlabel("Hour of Day")
ax3.set_ylabel("Number of Orders")
ax3.set_title("Order Time Distribution")
st.pyplot(fig3)

# 4. Top Departments
st.subheader("🏬 Top Departments by Number of Orders")
top_departments = prior_full['department'].value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(y=top_departments.index, x=top_departments.values, ax=ax4, palette='mako')
ax4.set_xlabel("Number of Orders")
ax4.set_ylabel("Department")
st.pyplot(fig4)

# 5. Heatmap of Day vs Hour
st.subheader("🧭 Heatmap: Orders by Day and Hour")
heatmap_data = orders.groupby(['order_dow', 'order_hour_of_day']).size().unstack()
fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', ax=ax5)
ax5.set_title("Orders Heatmap: Day of Week vs Hour of Day")
ax5.set_xlabel("Hour of Day")
ax5.set_ylabel("Day of Week (0=Sunday)")
st.pyplot(fig5)

# Footer
st.markdown("---")
st.markdown("✅ Built for Blinkit Strategy Intern — by [Your Name]")
