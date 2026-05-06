"""
05_dashboard_charts.py
────────────────────────────────────────────────────────────────────────
STEP 5: Generate all dashboard charts as PNG files.
  - Monthly revenue & profit trend
  - Category revenue breakdown (pie + bar)
  - RFM segment distribution
  - Cohort retention heatmap
  - Churn risk distribution
  - Top 10 products by profit
  - Regional performance

These PNGs can be directly pasted into Power BI, Tableau, or your README.

Run: python 05_dashboard_charts.py
Output: outputs/charts/*.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "outputs", "charts")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────
CLEAN   = os.path.join(BASE, "data",    "orders_clean.csv")
MONTHLY = os.path.join(BASE, "outputs", "kpis_monthly.csv")
CATEG   = os.path.join(BASE, "outputs", "kpis_category.csv")
REGION  = os.path.join(BASE, "outputs", "kpis_region.csv")
RFM     = os.path.join(BASE, "outputs", "rfm_segments.csv")
COHORT  = os.path.join(BASE, "outputs", "cohort_retention.csv")
CHURN   = os.path.join(BASE, "outputs", "churn_predictions.csv")

df      = pd.read_csv(CLEAN, parse_dates=["order_date"])
monthly = pd.read_csv(MONTHLY)
cat     = pd.read_csv(CATEG)
region  = pd.read_csv(REGION)
rfm     = pd.read_csv(RFM)

print("=" * 60)
print("  STEP 5 — GENERATING DASHBOARD CHARTS")
print("=" * 60)

# ── Style ─────────────────────────────────────────────────────────────
PALETTE  = ["#3266AD","#1D9E75","#EF9F27","#D85A30","#7B68EE","#E84393"]
BG       = "#F8FAFC"
DARK     = "#0D1B2A"
GRAY     = "#64748B"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.edgecolor":   "#E2E8F0", "axes.labelcolor": GRAY,
    "xtick.color": GRAY, "ytick.color": GRAY,
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.grid": True, "grid.alpha": 0.4, "grid.color": "#E2E8F0",
})

def save(name):
    path = os.path.join(OUT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"✅  Saved: outputs/charts/{name}")
    return path

# ── Chart 1: Monthly Revenue & Profit ──────────────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 5))
months = monthly["order_month"]
x      = range(len(months))
bars   = ax1.bar(x, monthly["revenue"] / 1e5, color=PALETTE[0], alpha=0.85, label="Revenue", width=0.6)
ax2    = ax1.twinx()
ax2.plot(x, monthly["profit_margin_%"], color=PALETTE[1], marker="o", linewidth=2.5,
         markersize=5, label="Profit Margin %")
ax1.set_xticks(list(x))
ax1.set_xticklabels(months, rotation=45, ha="right", fontsize=8)
ax1.set_ylabel("Revenue (₹ Lakhs)", color=PALETTE[0])
ax2.set_ylabel("Profit Margin %",   color=PALETTE[1])
ax1.yaxis.label.set_color(PALETTE[0])
ax1.tick_params(axis='y', colors=PALETTE[0])
ax2.tick_params(axis='y', colors=PALETTE[1])
fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.9), framealpha=0.8)
plt.title("Monthly Revenue & Profit Margin", fontsize=14, fontweight="bold", color=DARK, pad=12)
save("01_monthly_revenue.png")

# ── Chart 2: Category Revenue (horizontal bar) ─────────────────────────
fig, ax = plt.subplots(figsize=(9, 4))
colors  = PALETTE[:len(cat)]
bars    = ax.barh(cat["category"], cat["revenue"] / 1e5, color=colors, height=0.6)
for bar, val, pct in zip(bars, cat["revenue"] / 1e5, cat["revenue_share_%"]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"₹{val:.0f}L  ({pct}%)", va="center", fontsize=9, color=GRAY)
ax.set_xlabel("Revenue (₹ Lakhs)")
ax.grid(axis="y", alpha=0)
ax.invert_yaxis()
plt.title("Revenue by Category", fontsize=14, fontweight="bold", color=DARK, pad=12)
save("02_category_revenue.png")

# ── Chart 3: RFM Segment Distribution ─────────────────────────────────
seg_counts = rfm["Segment"].value_counts()
seg_rev    = rfm.groupby("Segment")["Monetary"].sum().reindex(seg_counts.index)
seg_colors = {
    "Champions":"#1D9E75","Loyal Customers":"#3266AD","Potential Loyalists":"#28A87D",
    "New Customers":"#EF9F27","Needs Attention":"#F59E0B","At Risk":"#D85A30","Lost":"#E74C3C"
}
colors = [seg_colors.get(s, "#888") for s in seg_counts.index]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.bar(seg_counts.index, seg_counts.values, color=colors, width=0.6)
ax1.set_xticklabels(seg_counts.index, rotation=35, ha="right", fontsize=8)
ax1.set_ylabel("Number of Customers")
ax1.set_title("Customers per Segment", fontsize=12, fontweight="bold", color=DARK)

ax2.bar(seg_rev.index, seg_rev.values / 1e5,
        color=[seg_colors.get(s,"#888") for s in seg_rev.index], width=0.6)
ax2.set_xticklabels(seg_rev.index, rotation=35, ha="right", fontsize=8)
ax2.set_ylabel("Revenue (₹ Lakhs)")
ax2.set_title("Revenue per Segment", fontsize=12, fontweight="bold", color=DARK)
plt.suptitle("RFM Customer Segmentation", fontsize=14, fontweight="bold", color=DARK, y=1.02)
plt.tight_layout()
save("03_rfm_segments.png")

# ── Chart 4: Cohort Retention Heatmap ─────────────────────────────────
cohort = pd.read_csv(COHORT)
cohort.set_index("Cohort", inplace=True)
month_cols = [c for c in cohort.columns if "Month" in c][:7]
heat_data  = cohort[month_cols].astype(float)

fig, ax = plt.subplots(figsize=(12, max(5, len(heat_data) * 0.4 + 1)))
import matplotlib.colors as mcolors
cmap = mcolors.LinearSegmentedColormap.from_list("ret", ["#F8FAFC","#B5D4F4","#3266AD"])
im   = ax.imshow(heat_data.values, aspect="auto", cmap=cmap, vmin=0, vmax=100)
ax.set_xticks(range(len(month_cols)))
ax.set_xticklabels([f"M+{i}" for i in range(len(month_cols))], fontsize=9)
ax.set_yticks(range(len(heat_data)))
ax.set_yticklabels(heat_data.index, fontsize=8)
for i in range(len(heat_data)):
    for j in range(len(month_cols)):
        val = heat_data.values[i, j]
        if not np.isnan(val):
            ax.text(j, i, f"{val:.0f}%", ha="center", va="center",
                    fontsize=7, color="white" if val > 50 else DARK)
plt.colorbar(im, ax=ax, label="Retention %", shrink=0.6)
ax.set_title("Customer Cohort Retention Heatmap", fontsize=14, fontweight="bold", color=DARK, pad=12)
save("04_cohort_retention.png")

# ── Chart 5: Churn Risk Distribution ──────────────────────────────────
if os.path.exists(CHURN):
    churn_df = pd.read_csv(CHURN)
    risk_counts = churn_df["churn_risk"].value_counts().reindex(["Low","Medium","High"])
    risk_colors = ["#1D9E75","#EF9F27","#D85A30"]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(risk_counts.index, risk_counts.values, color=risk_colors, width=0.5)
    for bar, val in zip(bars, risk_counts.values):
        pct = val / risk_counts.sum() * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                f"{val:,}\n({pct:.0f}%)", ha="center", fontsize=10, color=GRAY)
    ax.set_ylabel("Number of Customers")
    ax.set_xlabel("Churn Risk Level")
    plt.title("Customer Churn Risk Distribution", fontsize=14, fontweight="bold", color=DARK, pad=12)
    save("05_churn_risk.png")

# ── Chart 6: Top 10 Products ──────────────────────────────────────────
top_products = (df.groupby(["product_name","category"])
                .agg(profit=("profit","sum"), orders=("order_id","count"))
                .reset_index()
                .sort_values("profit", ascending=False)
                .head(10))
cat_color_map = {c:PALETTE[i] for i,c in enumerate(df["category"].unique())}
colors = [cat_color_map.get(c, "#888") for c in top_products["category"]]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(top_products["product_name"], top_products["profit"] / 1e3, color=colors, height=0.6)
for bar, val in zip(bars, top_products["profit"] / 1e3):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"₹{val:.0f}K", va="center", fontsize=9, color=GRAY)
ax.invert_yaxis()
ax.set_xlabel("Total Profit (₹ Thousands)")
handles = [mpatches.Patch(color=v, label=k) for k, v in cat_color_map.items()]
ax.legend(handles=handles, loc="lower right", fontsize=8)
plt.title("Top 10 Products by Profit", fontsize=14, fontweight="bold", color=DARK, pad=12)
save("06_top_products.png")

# ── Chart 7: Regional performance ────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
metrics = [("revenue","Revenue (₹L)", 1e5), ("orders","Orders",1), ("profit_margin_%","Margin %",1)]
for ax, (col, label, div) in zip(axes, metrics):
    vals = region[col] / div if div != 1 else region[col]
    ax.bar(region["region"], vals, color=PALETTE[:len(region)], width=0.5)
    ax.set_title(label, fontsize=11, fontweight="bold", color=DARK)
    ax.set_xlabel("Region", fontsize=9)
plt.suptitle("Regional Performance Overview", fontsize=14, fontweight="bold", color=DARK, y=1.02)
plt.tight_layout()
save("07_regional_performance.png")

print("\n" + "=" * 60)
print(f"  ALL CHARTS SAVED to outputs/charts/")
print("  STEP 5 COMPLETE ✅")
print("=" * 60)
