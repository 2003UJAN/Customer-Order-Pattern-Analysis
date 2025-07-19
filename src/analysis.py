import os
import pandas as pd

# File paths
data_dir = "data"
file_paths = {
    "orders.csv": os.path.join(data_dir, "orders.csv"),
    "products.csv": os.path.join(data_dir, "products.csv"),
    "order_products__prior.csv": os.path.join(data_dir, "order_products__prior.csv"),
    "order_products__train.csv": os.path.join(data_dir, "order_products__train.csv"),
    "aisles.csv": os.path.join(data_dir, "aisles.csv"),
    "departments.csv": os.path.join(data_dir, "departments.csv"),
}

# Kaggle links
file_links = {
    "orders.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=orders.csv",
    "products.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=products.csv",
    "order_products__prior.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=order_products__prior.csv",
    "order_products__train.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=order_products__train.csv",
    "aisles.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=aisles.csv",
    "departments.csv": "https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data?select=departments.csv",
}

# Check missing files
missing = [f for f, path in file_paths.items() if not os.path.exists(path)]

if missing:
    print("❌ Missing files. Please download the following from Kaggle and place them in the `data/` folder:\n")
    for f in missing:
        print(f"- {f}: {file_links[f]}")
    exit(1)

# Load all datasets
orders = pd.read_csv(file_paths["orders.csv"])
products = pd.read_csv(file_paths["products.csv"])
prior = pd.read_csv(file_paths["order_products__prior.csv"])
train = pd.read_csv(file_paths["order_products__train.csv"])
aisles = pd.read_csv(file_paths["aisles.csv"])
departments = pd.read_csv(file_paths["departments.csv"])

# Sample EDA
print("✅ Loaded all datasets successfully.")
print("Orders shape:", orders.shape)
print("Products shape:", products.shape)
print("Aisles shape:", aisles.shape)
print("Departments shape:", departments.shape)

top_aisles = (
    products.merge(prior, on="product_id")
            .merge(aisles, on="aisle_id")
            .groupby("aisle")["order_id"].count()
            .sort_values(ascending=False)
            .head(5)
)

print("\nTop 5 Aisles by Order Count:")
print(top_aisles)
