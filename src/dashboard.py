import streamlit as st
import plotly.express as px
import pandas as pd
from src.analysis import merge_data, generate_freq_items
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="E-Commerce Order Pattern Dashboard")

df = merge_data()

st.title("🛒 E-Commerce Customer Order Pattern Dashboard")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Aisle/Dept Insights", "🧠 Association Rules", "👥 Cohort Analysis", "📆 Retention"])

with tab1:
    st.subheader("Top 15 Most Ordered Products")
    top_products = df['product_name'].value_counts().head(15).reset_index()
    fig = px.bar(top_products, x='product_name', y='count', title='Most Ordered Products')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Department Distribution")
    dept_counts = df['department'].value_counts().reset_index()
    fig2 = px.pie(dept_counts, values='department', names='index', title='Orders by Department')
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Top Aisles by Department")
    aisle_dept = df.groupby(['department', 'aisle']).size().reset_index(name='count')
    fig3 = px.treemap(aisle_dept, path=['department', 'aisle'], values='count', title='Treemap of Aisle Usage by Department')
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Association Rules (Apriori)")
    support = st.slider("Minimum Support", min_value=0.005, max_value=0.05, value=0.01, step=0.005)
    freq_items, rules = generate_freq_items(df, min_support=support)
    st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

with tab4:
    st.subheader("Cohort Analysis (Order Day vs Hour)")
    cohort = df.groupby(['order_dow', 'order_hour_of_day']).size().reset_index(name='orders')
    fig4 = px.density_heatmap(cohort, x='order_hour_of_day', y='order_dow', z='orders', nbinsx=24, nbinsy=7, title="Cohort Heatmap")
    st.plotly_chart(fig4, use_container_width=True)

with tab5:
    st.subheader("Customer Retention")
    retention = df.groupby(['user_id', 'order_number'])['order_id'].count().reset_index()
    retention = retention.groupby('order_number')['user_id'].count().reset_index()
    fig5 = px.line(retention, x='order_number', y='user_id', title='User Retention Over Orders')
    st.plotly_chart(fig5, use_container_width=True)
