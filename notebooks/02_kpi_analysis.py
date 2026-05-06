"""
STEP 2: KPI Analysis
====================
Calculates all business KPIs and saves charts + CSV reports.

Usage:
    python notebooks/02_kpi_analysis.py

Input:  data/cleaned/orders_clean.csv
Output: outputs/kpi_monthly.csv
        outputs/kpi_summary.csv
        outputs/charts/revenue_trend.png
        outputs/charts/category_breakdown.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

CLEAN_DIR  = "data/cleaned"
OUTPUT_DIR = "outputs"
CHART_DIR  = os.path.join(OUTPUT_DIR,"charts")
os.makedirs(CHART_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
COLORS = ["#3266ad","#1d9e75","#ef9f27","#d85a30","#9b59b6"]

print("📂 Loading cleaned data...")
df = pd.read_csv(os.path.join(CLEAN_DIR,"orders_clean.csv"), parse_dates=["order_date"])
print(f"✅ {len(df):,} rows loaded")

# ── KPI 1: Monthly Revenue, Profit, Orders ─────────────────────────────
print("\n📊 Calculating monthly KPIs...")
monthly = df.groupby("order_month").agg(
    revenue  = ("revenue","sum"),
    profit   = ("profit","sum"),
    orders   = ("order_id","count"),
    customers= ("customer_id","nunique")
).reset_index()
monthly["margin_pct"] = (monthly["profit"]/monthly["revenue"]*100).round(1)
monthly["aov"]        = (monthly["revenue"]/monthly["orders"]).round(2)
monthly["mom_growth"] = monthly["revenue"].pct_change().mul(100).round(1)
monthly.to_csv(os.path.join(OUTPUT_DIR,"kpi_monthly.csv"), index=False)
print("   ✅ kpi_monthly.csv saved")

# ── KPI 2: Summary ─────────────────────────────────────────────────────
summary = {
    "Total Revenue":       f'₹{df["revenue"].sum():,.0f}',
    "Total Profit":        f'₹{df["profit"].sum():,.0f}',
    "Avg Profit Margin":   f'{df["profit_margin"].mean():.1f}%',
    "Total Orders":        f'{df["order_id"].nunique():,}',
    "Unique Customers":    f'{df["customer_id"].nunique():,}',
    "Avg Order Value":     f'₹{(df["revenue"].sum()/df["order_id"].nunique()):,.0f}',
}
pd.DataFrame(summary.items(),columns=["KPI","Value"]).to_csv(
    os.path.join(OUTPUT_DIR,"kpi_summary.csv"), index=False)
print("\n📋 KPI Summary:")
for k,v in summary.items():
    print(f"   {k:<22} {v}")

# ── Chart 1: Monthly Revenue Trend ────────────────────────────────────
fig, axes = plt.subplots(2,2, figsize=(14,10))
fig.suptitle("Sales Analytics — KPI Dashboard", fontsize=16, fontweight="bold", y=1.01)

ax = axes[0,0]
months = [str(m) for m in monthly["order_month"]]
ax.bar(months, monthly["revenue"]/1000, color=COLORS[0], alpha=0.85, zorder=3)
ax.set_title("Monthly Revenue (₹ thousands)", fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Revenue (₹K)")
ax.tick_params(axis="x", rotation=45)

ax = axes[0,1]
if "category" in df.columns:
    cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    ax.pie(cat_rev, labels=cat_rev.index, autopct="%1.1f%%",
           colors=COLORS[:len(cat_rev)], startangle=90)
    ax.set_title("Revenue by Category", fontweight="bold")
else:
    ax.text(0.5,0.5,"Category column\nnot in dataset", ha="center", va="center", transform=ax.transAxes)
    ax.set_title("Revenue by Category", fontweight="bold")

ax = axes[1,0]
ax.plot(months, monthly["margin_pct"], color=COLORS[1], marker="o", linewidth=2, markersize=5, zorder=3)
ax.fill_between(range(len(months)), monthly["margin_pct"], alpha=0.15, color=COLORS[1])
ax.set_title("Profit Margin % by Month", fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Margin %")
ax.set_xticks(range(len(months))); ax.set_xticklabels(months, rotation=45)

ax = axes[1,1]
ax.bar(months, monthly["orders"], color=COLORS[2], alpha=0.85, zorder=3)
ax.set_title("Orders per Month", fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Order Count")
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
chart_path = os.path.join(CHART_DIR,"kpi_dashboard.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n✅ Chart saved: {chart_path}")

# ── Chart 2: Category breakdown ────────────────────────────────────────
if "category" in df.columns:
    fig, axes = plt.subplots(1,2, figsize=(14,5))
    cat_stats = df.groupby("category").agg(
        revenue=("revenue","sum"), profit=("profit","sum"), orders=("order_id","count")
    ).reset_index()
    cat_stats["margin_pct"] = (cat_stats["profit"]/cat_stats["revenue"]*100).round(1)
    cat_stats.sort_values("revenue", ascending=True, inplace=True)

    ax = axes[0]
    ax.barh(cat_stats["category"], cat_stats["revenue"]/1000, color=COLORS[0], alpha=0.85)
    ax.set_title("Revenue by Category (₹K)", fontweight="bold")
    ax.set_xlabel("Revenue (₹ thousands)")

    ax = axes[1]
    ax.barh(cat_stats["category"], cat_stats["margin_pct"], color=COLORS[1], alpha=0.85)
    ax.set_title("Profit Margin % by Category", fontweight="bold")
    ax.set_xlabel("Margin %")

    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR,"category_breakdown.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Chart saved: outputs/charts/category_breakdown.png")

print("\n🎉 KPI Analysis complete! Check outputs/ folder.")
