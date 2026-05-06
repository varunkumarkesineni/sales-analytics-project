"""
STEP 1: Data Cleaning
=====================
Run this first before any other script.

Usage:
    python notebooks/01_data_cleaning.py

Input:  data/raw/online_retail_II.csv  (or .xlsx)
Output: data/cleaned/orders_clean.csv
"""

import pandas as pd
import numpy as np
import os

RAW_DIR   = "data/raw"
CLEAN_DIR = "data/cleaned"
os.makedirs(CLEAN_DIR, exist_ok=True)

print("📂 Loading dataset...")

raw_files  = os.listdir(RAW_DIR)
csv_files  = [f for f in raw_files if f.endswith(".csv")]
xlsx_files = [f for f in raw_files if f.endswith(".xlsx")]

if csv_files:
    df = pd.read_csv(os.path.join(RAW_DIR, csv_files[0]), encoding="latin1")
elif xlsx_files:
    df = pd.read_excel(os.path.join(RAW_DIR, xlsx_files[0]))
else:
    print("⚠️  No dataset found in data/raw/. Generating sample data for demo...")
    np.random.seed(42)
    n = 10000
    categories = ["Electronics","Clothing","Home & Kitchen","Books","Sports"]
    regions    = ["North","South","East","West"]
    dates      = pd.date_range("2023-01-01","2023-12-31", periods=n)
    df = pd.DataFrame({
        "InvoiceNo":   [f"INV{i:05d}" for i in range(n)],
        "CustomerID":  np.random.randint(1000,1500,n),
        "StockCode":   [f"PRD{i:03d}" for i in np.random.randint(1,200,n)],
        "Description": np.random.choice(["Laptop","T-Shirt","Kitchen Blender","Python Book",
                        "Cricket Bat","Smartphone","Jeans","Coffee Maker","Data Science Book","Football"],n),
        "Category":    np.random.choice(categories,n),
        "Region":      np.random.choice(regions,n),
        "Quantity":    np.random.randint(1,10,n),
        "UnitPrice":   np.round(np.random.uniform(50,5000,n),2),
        "InvoiceDate": dates,
        "Country":     np.random.choice(["India","USA","UK","Germany"],n),
    })
    df.loc[np.random.choice(df.index,200),"CustomerID"] = np.nan
    df.loc[np.random.choice(df.index,50),"UnitPrice"]   = np.nan
    df = pd.concat([df, df.sample(100)], ignore_index=True)

print(f"✅ Loaded {len(df):,} rows, {df.shape[1]} columns")

rename_map = {
    "Invoice":"order_id","InvoiceNo":"order_id","Customer ID":"customer_id",
    "CustomerID":"customer_id","StockCode":"product_id","Description":"product_name",
    "Category":"category","Region":"region","Quantity":"quantity",
    "Price":"unit_price","UnitPrice":"unit_price","InvoiceDate":"order_date","Country":"country",
}
df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns}, inplace=True)

before = len(df)
df.drop_duplicates(inplace=True)
print(f"🗑️  Removed {before-len(df)} duplicates")

critical = [c for c in ["customer_id","order_id","unit_price","quantity"] if c in df.columns]
before = len(df)
df.dropna(subset=critical, inplace=True)
print(f"🗑️  Dropped {before-len(df)} null rows")

if "order_id" in df.columns:
    before = len(df)
    df = df[~df["order_id"].astype(str).str.startswith("C")]
    print(f"🗑️  Removed {before-len(df)} cancellations")

df = df[(df["quantity"]>0) & (df["unit_price"]>0)]

if "order_date" in df.columns:
    df["order_date"]    = pd.to_datetime(df["order_date"], errors="coerce")
    df.dropna(subset=["order_date"], inplace=True)
    df["order_month"]   = df["order_date"].dt.to_period("M")
    df["order_quarter"] = df["order_date"].dt.to_period("Q")
    df["order_year"]    = df["order_date"].dt.year
    df["order_dow"]     = df["order_date"].dt.day_name()

df["revenue"] = df["quantity"] * df["unit_price"]
if "cost" not in df.columns:
    np.random.seed(0)
    df["cost"] = df["revenue"] * np.random.uniform(0.6,0.85,len(df))
df["profit"]        = df["revenue"] - df["cost"]
df["profit_margin"] = (df["profit"]/df["revenue"]*100).round(2)

Q1,Q3 = df["revenue"].quantile([0.25,0.75])
IQR   = Q3-Q1
before = len(df)
df = df[(df["revenue"]>=Q1-1.5*IQR)&(df["revenue"]<=Q3+1.5*IQR)]
print(f"🗑️  Removed {before-len(df)} outliers")

if "customer_id" in df.columns:
    df["customer_id"] = df["customer_id"].astype(int).astype(str)

output = os.path.join(CLEAN_DIR,"orders_clean.csv")
df.to_csv(output, index=False)

print(f"\n✅ Saved: {output}")
print(f"📊 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"   Total Revenue   : ₹{df['revenue'].sum():,.0f}")
print(f"   Total Profit    : ₹{df['profit'].sum():,.0f}")
print(f"   Avg Margin      : {df['profit_margin'].mean():.1f}%")
print(f"   Unique Customers: {df['customer_id'].nunique():,}")
