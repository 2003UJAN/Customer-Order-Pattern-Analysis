import streamlit as st
import plotly.express as px
from analysis import get_time_data, get_top_items, get_rules

st.set_page_config(page_title="Order Patterns", layout="wide")
st.title("🛒 Customer Order Pattern Analysis")
st.markdown("Explore Instacart data to identify order timing, popular products, and bundle patterns.")

# Load processed data
time_df = get_time_data()
top_items = get_top_items()
rules = get_rules()

# Section: Peak Ordering Times
st.subheader("⏰ Peak Ordering Times")
fig1 = px.density_heatmap(
    time_df,
    x='order_hour_of_day',
    y='order_dow',
    z='order_count',
    color_continuous_scale='Turbo',
    labels={'order_dow': 'Day of Week', 'order_hour_of_day': 'Hour'},
    nbinsx=24,
    nbinsy=7
)
st.plotly_chart(fig1, use_container_width=True)

# Section: Top Products
st.subheader("🏆 Top 20 Most Ordered Products")
fig2 = px.bar(
    top_items,
    x='order_count',
    y='product_name',
    orientation='h',
    labels={'product_name': 'Product', 'order_count': 'Order Count'},
    height=600
)
fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig2, use_container_width=True)

# Section: Association Rules
st.subheader("🔗 Frequently Bought Together (Market Basket Rules)")
st.dataframe(rules.style.format({'support': '{:.2%}', 'confidence': '{:.2%}', 'lift': '{:.2f}'}))
