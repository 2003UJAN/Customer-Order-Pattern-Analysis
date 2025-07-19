import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from src.analysis import load_data, merge_data, generate_freq_items, top_products, reorder_ratio

st.set_page_config(layout="wide", page_title="Instacart Customer Order Analysis")

st.title("🛒 Instacart Market Basket Analysis Dashboard")

# Load and preprocess
data = load_data()
merged = merge_data(data)

st.sidebar.header("Filters")
min_support = st.sidebar.slider("Min Support for Apriori", 0.005, 0.1, 0.02)

# Top selling products
st.subheader("📦 Top 10 Most Ordered Products")
top_items = top_products(merged)
st.bar_chart(top_items)

# Reorder ratio
st.subheader("🔁 Top 10 Reordered Products")
reorder = reorder_ratio(merged)
fig, ax = plt.subplots()
sns.barplot(x=reorder.values, y=reorder.index, ax=ax)
st.pyplot(fig)

# Word cloud of product names
st.subheader("☁️ Word Cloud of Product Names")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(merged['product_name']))
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Treemap of departments and aisles
st.subheader("📊 Treemap: Products by Department and Aisle")
treemap_df = merged.groupby(['department', 'aisle'])['product_id'].count().reset_index()
treemap_df.columns = ['Department', 'Aisle', 'Count']
fig = px.treemap(treemap_df, path=['Department', 'Aisle'], values='Count', color='Department')
st.plotly_chart(fig, use_container_width=True)

# Association Rule Mining
st.subheader("🧠 Association Rules from Apriori")
freq_items, rules = generate_freq_items(merged, min_support=min_support)

st.write("Frequent Itemsets:")
st.dataframe(freq_items.sort_values(by='support', ascending=False).head(10))

st.write("Top Association Rules:")
st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

# Support vs Confidence plot
fig = px.scatter(rules, x='support', y='confidence', size='lift', color='lift', hover_data=['antecedents', 'consequents'])
st.plotly_chart(fig, use_container_width=True)
