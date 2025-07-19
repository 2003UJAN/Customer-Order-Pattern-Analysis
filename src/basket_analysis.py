from mlxtend.frequent_patterns import apriori, association_rules

def compute_basket(order_products, products, n_orders=5000):
    # Limit number of orders for memory efficiency
    order_ids = order_products['order_id'].unique()[:n_orders]
    merged = order_products[order_products['order_id'].isin(order_ids)].merge(products, on='product_id')
    basket = merged.groupby(['order_id', 'product_name'])['add_to_cart_order'].count().unstack().fillna(0)
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    return basket

def get_market_basket_rules(basket, support=0.02, min_lift=1.2):
    freq = apriori(basket, min_support=support, use_colnames=True)
    rules = association_rules(freq, metric="lift", min_threshold=min_lift)
    keep_cols = ['antecedents', 'consequents', 'support', 'confidence', 'lift']
    rules[keep_cols] = rules[keep_cols]
    # Convert frozensets to strings for display
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    return rules.sort_values('lift', ascending=False)
