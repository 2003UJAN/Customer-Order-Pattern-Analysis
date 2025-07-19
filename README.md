# 🛒 E-Commerce Customer Order Pattern Analysis

This project analyzes grocery delivery order behavior using the Instacart Market Basket dataset.  
It explores:

- Peak ordering times (day/hour)
- Most frequently ordered items
- Product bundling patterns using association rules

## 📊 Tech Stack

- Python (Pandas, Plotly)
- Streamlit dashboard
- Association Rule Mining with mlxtend
- Dataset: Instacart Market Basket Analysis

## 📥 Dataset

Download the dataset from Kaggle (you'll need a Kaggle account):

🔗 [Instacart Market Basket Analysis](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis)

Place the downloaded CSV files in the `data/` folder.

## ▶️ Run Locally

```bash
git clone https://github.com/2003UJAN/E-Commerce-Customer-Order-Pattern-Analysis.git
cd blinkit-order-pattern-analysis
pip install -r requirements.txt
streamlit run src/dashboard.py
