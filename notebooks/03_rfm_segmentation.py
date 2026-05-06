"""
STEP 3: RFM Customer Segmentation
===================================
Segments customers into Champions, Loyal, At Risk, Lost.

Usage:
    python notebooks/03_rfm_segmentation.py

Input:  data/cleaned/orders_clean.csv
Output: outputs/rfm_segments.csv
        outputs/charts/rfm_segmentation.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

CLEAN_DIR  = "data/cleaned"
OUTPUT_DIR = "outputs"
CHART_DIR  = os.path.join(OUTPUT_DIR,"charts")
os.makedirs(CHART_DIR, exist_ok=True)

print("📂 Loading cleaned data...")
df = pd.read_csv(os.path.join(CLEAN_DIR,"orders_clean.csv"), parse_dates=["order_date"])

snapshot_date = df["order_date"].max()
print(f"📅 Snapshot date: {snapshot_date.date()}")

# ── Calculate RFM metrics ──────────────────────────────────────────────
print("\n⚙️  Calculating RFM metrics...")
rfm = df.groupby("customer_id").agg(
    Recency   = ("order_date",  lambda x: (snapshot_date - x.max()).days),
    Frequency = ("order_id",    "count"),
    Monetary  = ("revenue",     "sum")
).reset_index()

# ── Score 1–5 using quintiles ──────────────────────────────────────────
rfm["R_score"] = pd.qcut(rfm["Recency"],   q=5, labels=[5,4,3,2,1], duplicates="drop").astype(int)
rfm["F_score"] = pd.qcut(rfm["Frequency"], q=5, labels=[1,2,3,4,5], duplicates="drop").astype(int)
rfm["M_score"] = pd.qcut(rfm["Monetary"],  q=5, labels=[1,2,3,4,5], duplicates="drop").astype(int)
rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

# ── Assign segments ────────────────────────────────────────────────────
def assign_segment(score):
    if score >= 12: return "Champions"
    if score >= 9:  return "Loyal Customers"
    if score >= 6:  return "At Risk"
    return "Lost / Inactive"

rfm["Segment"] = rfm["RFM_score"].apply(assign_segment)

# ── Segment summary ────────────────────────────────────────────────────
seg_summary = rfm.groupby("Segment").agg(
    Customers     = ("customer_id","count"),
    Avg_Recency   = ("Recency","mean"),
    Avg_Frequency = ("Frequency","mean"),
    Avg_Monetary  = ("Monetary","mean"),
    Total_Revenue = ("Monetary","sum")
).reset_index().round(1)
seg_summary["Revenue_Share_%"] = (seg_summary["Total_Revenue"]/seg_summary["Total_Revenue"].sum()*100).round(1)
seg_summary.sort_values("Total_Revenue", ascending=False, inplace=True)

print("\n📊 RFM Segment Summary:")
print(seg_summary.to_string(index=False))

# ── Save ───────────────────────────────────────────────────────────────
rfm.to_csv(os.path.join(OUTPUT_DIR,"rfm_segments.csv"), index=False)
seg_summary.to_csv(os.path.join(OUTPUT_DIR,"rfm_segment_summary.csv"), index=False)
print(f"\n✅ Saved: outputs/rfm_segments.csv")

# ── Chart ──────────────────────────────────────────────────────────────
seg_colors = {"Champions":"#1d9e75","Loyal Customers":"#3266ad",
              "At Risk":"#ef9f27","Lost / Inactive":"#d85a30"}

fig, axes = plt.subplots(1,3, figsize=(16,5))
fig.suptitle("RFM Customer Segmentation", fontsize=14, fontweight="bold")

# Pie — customer count
ax = axes[0]
counts = rfm["Segment"].value_counts()
colors = [seg_colors[s] for s in counts.index]
ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=colors, startangle=90)
ax.set_title("Customer Count by Segment")

# Bar — revenue share
ax = axes[1]
seg_s = seg_summary.set_index("Segment")
bars  = ax.bar(seg_s.index, seg_s["Revenue_Share_%"],
               color=[seg_colors[s] for s in seg_s.index], alpha=0.85, zorder=3)
ax.bar_label(bars, fmt="%.1f%%", padding=3)
ax.set_title("Revenue Share by Segment")
ax.set_ylabel("Revenue %")
ax.tick_params(axis="x", rotation=15)

# Scatter — Recency vs Monetary
ax = axes[2]
for seg, grp in rfm.groupby("Segment"):
    ax.scatter(grp["Recency"], grp["Monetary"], c=seg_colors[seg],
               label=seg, alpha=0.5, s=20, zorder=3)
ax.set_title("Recency vs Monetary Value")
ax.set_xlabel("Recency (days since last order)")
ax.set_ylabel("Total Monetary Value (₹)")
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR,"rfm_segmentation.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart saved: outputs/charts/rfm_segmentation.png")

# ── Action recommendations ─────────────────────────────────────────────
print("\n💡 Recommended Actions by Segment:")
actions = {
    "Champions":       "Reward them. Ask for reviews. Offer referral bonuses.",
    "Loyal Customers": "Upsell higher-value products. Enroll in loyalty program.",
    "At Risk":         "Send re-engagement email with 10-15% discount coupon.",
    "Lost / Inactive": "Win-back campaign with heavy discount. Else remove from budget.",
}
for seg, action in actions.items():
    count = (rfm["Segment"]==seg).sum()
    print(f"   {seg:<20} ({count:,} customers): {action}")

print("\n🎉 RFM Segmentation complete!")
