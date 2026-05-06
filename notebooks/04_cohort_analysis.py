"""
STEP 4: Cohort Retention Analysis
===================================
Builds a cohort retention heatmap — the #1 most impressive chart for interviews.

Usage:
    python notebooks/04_cohort_analysis.py

Input:  data/cleaned/orders_clean.csv
Output: outputs/cohort_table.csv
        outputs/charts/cohort_heatmap.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

CLEAN_DIR  = "data/cleaned"
OUTPUT_DIR = "outputs"
CHART_DIR  = os.path.join(OUTPUT_DIR,"charts")
os.makedirs(CHART_DIR, exist_ok=True)

print("📂 Loading cleaned data...")
df = pd.read_csv(os.path.join(CLEAN_DIR,"orders_clean.csv"), parse_dates=["order_date"])

# ── Cohort month = first purchase month per customer ───────────────────
print("⚙️  Building cohort table...")
df["order_month_dt"]  = df["order_date"].dt.to_period("M").dt.to_timestamp()
df["cohort_month"]    = df.groupby("customer_id")["order_date"].transform("min").dt.to_period("M").dt.to_timestamp()
df["month_number"]    = ((df["order_month_dt"].dt.year  - df["cohort_month"].dt.year)*12 +
                         (df["order_month_dt"].dt.month - df["cohort_month"].dt.month))

# ── Build cohort pivot table ───────────────────────────────────────────
cohort_data = df.groupby(["cohort_month","month_number"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index="cohort_month", columns="month_number", values="customer_id")

# ── Calculate retention % ──────────────────────────────────────────────
cohort_size   = cohort_pivot[0]
retention_pct = cohort_pivot.divide(cohort_size, axis=0).round(3) * 100

# ── Format index ──────────────────────────────────────────────────────
retention_pct.index = retention_pct.index.strftime("%Y-%m")
cohort_pivot.index  = cohort_pivot.index.strftime("%Y-%m")

# ── Save ───────────────────────────────────────────────────────────────
retention_pct.to_csv(os.path.join(OUTPUT_DIR,"cohort_table.csv"))
print("✅ Saved: outputs/cohort_table.csv")

# ── Print summary ──────────────────────────────────────────────────────
print(f"\n📊 Cohort Retention Summary (first 6 months):")
display_cols = [c for c in range(7) if c in retention_pct.columns]
print(retention_pct[display_cols].round(1).to_string())

month1_retention = retention_pct[1].dropna().mean() if 1 in retention_pct.columns else 0
month3_retention = retention_pct[3].dropna().mean() if 3 in retention_pct.columns else 0
print(f"\n   Avg Month-1 Retention: {month1_retention:.1f}%")
print(f"   Avg Month-3 Retention: {month3_retention:.1f}%")

# ── Heatmap ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14,7))

max_months = min(12, len(retention_pct.columns))
plot_data  = retention_pct.iloc[:, :max_months].fillna(0)

cmap = plt.cm.YlOrRd_r
im   = ax.imshow(plot_data.values, cmap=cmap, aspect="auto", vmin=0, vmax=100)

# Annotate cells
for i in range(len(plot_data)):
    for j in range(len(plot_data.columns)):
        val = plot_data.values[i,j]
        if val > 0:
            text_color = "white" if val < 40 else "black"
            ax.text(j, i, f"{val:.0f}%", ha="center", va="center",
                    fontsize=9, color=text_color, fontweight="bold")

ax.set_xticks(range(len(plot_data.columns)))
ax.set_xticklabels([f"Month {c}" for c in plot_data.columns], rotation=45, ha="right")
ax.set_yticks(range(len(plot_data)))
ax.set_yticklabels(plot_data.index)
ax.set_title("Customer Cohort Retention Heatmap\n(% of cohort still active)", 
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Months Since First Purchase")
ax.set_ylabel("Cohort (First Purchase Month)")

cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Retention %", rotation=270, labelpad=15)

plt.tight_layout()
heatmap_path = os.path.join(CHART_DIR,"cohort_heatmap.png")
plt.savefig(heatmap_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n✅ Heatmap saved: {heatmap_path}")
print("\n💡 Tip: This cohort heatmap is your most powerful interview visual. Explain it as:")
print("   'Row = when customer first bought. Column = months later. Value = % still buying.'")
print("\n🎉 Cohort Analysis complete!")
