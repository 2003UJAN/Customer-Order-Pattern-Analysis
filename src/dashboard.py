import streamlit as st
from analysis import download_data, analyze_data

st.set_page_config(page_title="E-Commerce Order Patterns", layout="wide")

st.title("📦 E-Commerce Customer Order Pattern Dashboard")

if st.button("🔽 Download Instacart Data"):
    with st.spinner("Downloading..."):
        download_data()
    st.success("Data downloaded successfully!")

st.subheader("📊 Top 10 Most Reordered Products")
top_products = analyze_data()
st.bar_chart(top_products)
