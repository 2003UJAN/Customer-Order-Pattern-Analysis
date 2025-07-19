import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analysis import load_data, merge_data, generate_freq_items, top_products, reorder_ratio

st.set_page_config(layout="wide", page_title="Instacart Order Pattern Dashboard")

st.title("🛒 Instacart E-Commerce Order Analysis")

with st.spinner("Loading data..."):
    dfs = load_data()
    merged_df = merge_data(dfs)

st.sidebar.header("Navigation")
choice = st.sidebar.radio("Select Analysis", ["Overview", "Top Products", "Reorder Ratios", "Frequent Itemsets", "Treemap"])

if choice == "Overview":
    st.subheader("Data Overview")
    st.dataframe(merged_df.sample(1000))

elif choice == "Top Products":
    st.subheader("Top Selling Products")
    top_df = top_products(merged_df)
    fig = px.bar(top_df, x='product_name', y='count', title="Top 10 Products", labels={'count': 'Number of Orders'})
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Reorder Ratios":
    st.subheader("Most Reordered Products")
    reorder_df = reorder_ratio(merged_df)
    fig = px.bar(reorder_df, x='product_name', y='reorder_ratio', title="Top Reordered Products")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Frequent Itemsets":
    st.subheader("Frequent Product Combinations")
    freq_items = generate_freq_items(merged_df)
    st.dataframe(freq_items.sort_values('support', ascending=False).head(10))

elif choice == "Treemap":
    st.subheader("Product Sales Treemap by Department")
    dept_prod = (merged_df.groupby(['department', 'product_name'])
                 .size()
                 .reset_index(name='count'))
    fig = px.treemap(dept_prod, path=['department', 'product_name'], values='count',
                     title="Treemap of Products in Departments")
    st.plotly_chart(fig, use_container_width=True)
