import streamlit as st
import plotly.express as px
from src.analysis import load_data, merge_data, reorder_ratio, top_products, generate_freq_items

st.set_page_config(page_title="E-Commerce Order Pattern Dashboard", layout="wide")

st.title("🛒 E-Commerce Customer Order Pattern Dashboard")

# Load and merge data
dfs = load_data()
data = merge_data(dfs)

# Sidebar Filters
st.sidebar.header("Filter Options")
departments = st.sidebar.multiselect("Select Department", sorted(data["department"].unique()), default=None)
if departments:
    data = data[data["department"].isin(departments)]

# Top Products
st.subheader("Top 10 Most Ordered Products")
top = top_products(data)
fig1 = px.bar(top, x=top.index, y=top.values, labels={"x": "Product", "y": "Order Count"})
st.plotly_chart(fig1, use_container_width=True)

# Reorder Ratios
st.subheader("Top Reordered Products")
reorder = reorder_ratio(data).head(10)
fig2 = px.bar(reorder, x=reorder.index, y=reorder.values, labels={"x": "Product", "y": "Reorder Ratio"})
st.plotly_chart(fig2, use_container_width=True)

# Pie Chart by Department
st.subheader("Product Distribution by Department")
dept_counts = data["department"].value_counts().nlargest(10)
fig3 = px.pie(values=dept_counts.values, names=dept_counts.index)
st.plotly_chart(fig3, use_container_width=True)

# Association Rules
st.subheader("Association Rules")
frequent_itemsets, rules = generate_freq_items(data)
st.dataframe(rules[["antecedents", "consequents", "support", "confidence", "lift"]].head(10))

# Treemap by Aisle
st.subheader("Treemap of Product Orders by Aisle")
aisle_counts = data.groupby(["department", "aisle"]).size().reset_index(name='count')
fig4 = px.treemap(aisle_counts, path=["department", "aisle"], values="count")
st.plotly_chart(fig4, use_container_width=True)
