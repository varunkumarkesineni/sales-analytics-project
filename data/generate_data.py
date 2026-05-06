"""
generate_data.py
Generates a realistic synthetic e-commerce dataset (50,000 orders).
Run this FIRST before any other script.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# ── Config ─────────────────────────────────────────────────────────────
N_ORDERS      = 50_000
N_CUSTOMERS   = 8_000
START_DATE    = datetime(2022, 1, 1)
END_DATE      = datetime(2023, 12, 31)

CATEGORIES = {
    "Electronics": {"products": ["Smartphone","Laptop","Earbuds","Smartwatch","Tablet","Camera","Router","SSD"],
                    "price_range": (500, 80000), "cost_pct": (0.55, 0.72), "weight": 0.28},
    "Clothing":    {"products": ["T-Shirt","Jeans","Kurta","Jacket","Sneakers","Saree","Hoodie","Shorts"],
                    "price_range": (199, 5000),  "cost_pct": (0.35, 0.55), "weight": 0.22},
    "Home & Kitchen":{"products":["Pressure Cooker","Mixer","Air Fryer","Bedsheet","Curtains","Lamp","Mug Set","Knife Set"],
                    "price_range": (299, 12000), "cost_pct": (0.40, 0.60), "weight": 0.18},
    "Books":       {"products": ["Data Science Book","Python Guide","MBA Prep","Fiction Novel","Self-Help","Cookbook"],
                    "price_range": (149, 1200),  "cost_pct": (0.20, 0.35), "weight": 0.12},
    "Sports":      {"products": ["Yoga Mat","Dumbbell","Cricket Bat","Football","Resistance Band","Skipping Rope"],
                    "price_range": (199, 8000),  "cost_pct": (0.38, 0.55), "weight": 0.10},
    "Beauty":      {"products": ["Face Cream","Perfume","Shampoo","Lipstick","Sunscreen","Serum"],
                    "price_range": (99, 3000),   "cost_pct": (0.30, 0.48), "weight": 0.10},
}

REGIONS = {
    "North": ["Delhi","Chandigarh","Lucknow","Jaipur","Agra"],
    "South": ["Bangalore","Chennai","Hyderabad","Kochi","Coimbatore"],
    "East":  ["Kolkata","Bhubaneswar","Patna","Guwahati","Ranchi"],
    "West":  ["Mumbai","Pune","Ahmedabad","Surat","Nagpur"],
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery", "Wallet"]

# ── Generate customers ──────────────────────────────────────────────────
regions_flat   = [(r, c) for r, cities in REGIONS.items() for c in cities]
customer_ids   = [f"CUST{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS+1)]
customer_data  = []
for cid in customer_ids:
    region, city = random.choice(regions_flat)
    customer_data.append({
        "customer_id": cid,
        "customer_name": f"Customer_{cid[-4:]}",
        "email": f"{cid.lower()}@example.com",
        "city": city,
        "region": region,
        "signup_date": START_DATE + timedelta(days=random.randint(0, 400)),
        "age_group": random.choice(["18-24","25-34","35-44","45-54","55+"]),
        "gender": random.choice(["M","F","Other"]),
    })
customers_df = pd.DataFrame(customer_data)

# ── Generate orders ─────────────────────────────────────────────────────
cat_names    = list(CATEGORIES.keys())
cat_weights  = [CATEGORIES[c]["weight"] for c in cat_names]

orders = []
for i in range(N_ORDERS):
    order_date  = START_DATE + timedelta(days=random.randint(0, (END_DATE-START_DATE).days))
    ship_days   = random.choices([1,2,3,4,5,7,10], weights=[5,15,25,25,15,10,5])[0]
    ship_date   = order_date + timedelta(days=ship_days)

    cat_name    = random.choices(cat_names, weights=cat_weights)[0]
    cat         = CATEGORIES[cat_name]
    product     = random.choice(cat["products"])
    quantity    = random.choices([1,2,3,4,5], weights=[55,25,12,5,3])[0]
    unit_price  = round(random.uniform(*cat["price_range"]), 2)
    revenue     = round(unit_price * quantity, 2)
    cost_pct    = random.uniform(*cat["cost_pct"])
    cost        = round(revenue * cost_pct, 2)
    profit      = round(revenue - cost, 2)

    customer    = random.choice(customer_ids)
    is_returned = random.random() < 0.073   # 7.3% return rate
    rating      = random.choices([1,2,3,4,5], weights=[3,5,12,40,40])[0]
    if is_returned:
        rating  = random.choices([1,2,3], weights=[50,30,20])[0]

    orders.append({
        "order_id":       f"ORD{str(i+1).zfill(6)}",
        "customer_id":    customer,
        "order_date":     order_date.strftime("%Y-%m-%d"),
        "ship_date":      ship_date.strftime("%Y-%m-%d"),
        "category":       cat_name,
        "product_name":   product,
        "quantity":       quantity,
        "unit_price":     unit_price,
        "revenue":        revenue,
        "cost":           cost,
        "profit":         profit,
        "payment_method": random.choice(PAYMENT_METHODS),
        "is_returned":    int(is_returned),
        "rating":         rating,
    })

orders_df = pd.DataFrame(orders)

# Merge region info onto orders
orders_df = orders_df.merge(customers_df[["customer_id","city","region"]], on="customer_id", how="left")

# Save
out_dir = os.path.dirname(os.path.abspath(__file__))
orders_df.to_csv(os.path.join(out_dir, "orders_raw.csv"), index=False)
customers_df.to_csv(os.path.join(out_dir, "customers.csv"), index=False)

print(f"✅  Generated {len(orders_df):,} orders  |  {len(customers_df):,} customers")
print(f"    Saved → data/orders_raw.csv  &  data/customers.csv")
print(f"    Date range: {orders_df['order_date'].min()} → {orders_df['order_date'].max()}")
print(f"    Total revenue: ₹{orders_df['revenue'].sum():,.0f}")
