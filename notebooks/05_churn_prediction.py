"""
STEP 5: Churn Prediction Model
================================
Predicts which customers will churn using Random Forest.
Outputs churn probability scores for each customer.

Usage:
    python notebooks/05_churn_prediction.py

Input:  data/cleaned/orders_clean.csv
Output: outputs/churn_predictions.csv
        outputs/charts/churn_model.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble         import RandomForestClassifier
from sklearn.linear_model     import LogisticRegression
from sklearn.model_selection  import train_test_split
from sklearn.metrics          import (classification_report, confusion_matrix,
                                       roc_auc_score, roc_curve)
from sklearn.preprocessing    import StandardScaler
import os, warnings
warnings.filterwarnings("ignore")

CLEAN_DIR  = "data/cleaned"
OUTPUT_DIR = "outputs"
CHART_DIR  = os.path.join(OUTPUT_DIR,"charts")
os.makedirs(CHART_DIR, exist_ok=True)

print("📂 Loading cleaned data...")
df = pd.read_csv(os.path.join(CLEAN_DIR,"orders_clean.csv"), parse_dates=["order_date"])

snapshot = df["order_date"].max()
CHURN_DAYS = 90   # customer is "churned" if no purchase in last 90 days

# ── Feature engineering per customer ──────────────────────────────────
print("⚙️  Engineering customer features...")
features = df.groupby("customer_id").agg(
    total_orders     = ("order_id",   "count"),
    total_revenue    = ("revenue",    "sum"),
    avg_order_value  = ("revenue",    "mean"),
    total_quantity   = ("quantity",   "sum"),
    avg_profit_margin= ("profit_margin","mean"),
    days_since_first = ("order_date", lambda x: (snapshot - x.min()).days),
    days_since_last  = ("order_date", lambda x: (snapshot - x.max()).days),
    unique_products  = ("product_id", "nunique"),
).reset_index()

# Purchase frequency & recency trend
features["purchase_freq"] = features["total_orders"] / (features["days_since_first"].clip(1) / 30)
features["is_churned"]    = (features["days_since_last"] >= CHURN_DAYS).astype(int)

print(f"   Total customers : {len(features):,}")
print(f"   Churned         : {features['is_churned'].sum():,} ({features['is_churned'].mean()*100:.1f}%)")
print(f"   Active          : {(features['is_churned']==0).sum():,}")

# ── Model training ─────────────────────────────────────────────────────
FEATURE_COLS = ["total_orders","total_revenue","avg_order_value","avg_profit_margin",
                "days_since_first","days_since_last","purchase_freq","unique_products"]

X = features[FEATURE_COLS].fillna(0)
y = features["is_churned"]

X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler    = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# Random Forest
print("\n🤖 Training Random Forest...")
rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42, class_weight="balanced")
rf.fit(X_train, y_train)
rf_proba = rf.predict_proba(X_test)[:,1]
rf_pred  = rf.predict(X_test)
rf_auc   = roc_auc_score(y_test, rf_proba)

# Logistic Regression
print("🤖 Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
lr.fit(X_train_s, y_train)
lr_proba = lr.predict_proba(X_test_s)[:,1]
lr_auc   = roc_auc_score(y_test, lr_proba)

print(f"\n📊 Model Performance:")
print(f"   Random Forest AUC     : {rf_auc:.3f}")
print(f"   Logistic Regression AUC: {lr_auc:.3f}")
print(f"\n📋 Random Forest Classification Report:")
print(classification_report(y_test, rf_pred, target_names=["Active","Churned"]))

# ── Feature importance ─────────────────────────────────────────────────
feat_imp = pd.Series(rf.feature_importances_, index=FEATURE_COLS).sort_values(ascending=False)

# ── Predict on all customers ───────────────────────────────────────────
features["churn_probability"] = rf.predict_proba(X[FEATURE_COLS].fillna(0))[:,1].round(3)
features["churn_risk"]        = pd.cut(features["churn_probability"],
                                        bins=[0,0.3,0.6,1.0],
                                        labels=["Low Risk","Medium Risk","High Risk"])
features.to_csv(os.path.join(OUTPUT_DIR,"churn_predictions.csv"), index=False)
print(f"\n✅ Saved: outputs/churn_predictions.csv")

# ── High-risk customers ────────────────────────────────────────────────
high_risk = features[features["churn_risk"]=="High Risk"].sort_values("churn_probability",ascending=False)
print(f"\n🚨 High-Risk Customers: {len(high_risk):,}")
print(f"   Avg Revenue from High-Risk: ₹{high_risk['total_revenue'].mean():,.0f}")
print(high_risk[["customer_id","days_since_last","total_revenue","churn_probability"]].head(5).to_string(index=False))

# ── Charts ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2,2, figsize=(14,10))
fig.suptitle("Churn Prediction Model", fontsize=14, fontweight="bold")

# ROC Curve
ax = axes[0,0]
for model_name, fpr_arr, tpr_arr, auc_val in [
    ("Random Forest",        *roc_curve(y_test,rf_proba)[:2], rf_auc),
    ("Logistic Regression",  *roc_curve(y_test,lr_proba)[:2], lr_auc),
]:
    fpr_v,tpr_v,_ = roc_curve(y_test, rf_proba if "Forest" in model_name else lr_proba)
    ax.plot(fpr_v, tpr_v, label=f"{model_name} (AUC={auc_val:.2f})", linewidth=2)
ax.plot([0,1],[0,1],"k--",alpha=0.4)
ax.set_title("ROC Curve"); ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
ax.legend(); ax.set_xlim(0,1); ax.set_ylim(0,1.02)

# Feature importance
ax = axes[0,1]
ax.barh(feat_imp.index[::-1], feat_imp.values[::-1], color="#3266ad", alpha=0.85)
ax.set_title("Feature Importance (Random Forest)")
ax.set_xlabel("Importance Score")

# Churn risk distribution
ax = axes[1,0]
risk_counts = features["churn_risk"].value_counts()
ax.bar(risk_counts.index, risk_counts.values,
       color=["#1d9e75","#ef9f27","#d85a30"], alpha=0.85, zorder=3)
ax.set_title("Customers by Churn Risk Level")
ax.set_xlabel("Risk Level"); ax.set_ylabel("Number of Customers")
for i,(idx,val) in enumerate(risk_counts.items()):
    ax.text(i, val+2, str(val), ha="center", fontweight="bold")

# Churn prob distribution
ax = axes[1,1]
ax.hist(features["churn_probability"], bins=30, color="#3266ad", alpha=0.75, edgecolor="white")
ax.axvline(0.5, color="#d85a30", linestyle="--", linewidth=2, label="Threshold=0.5")
ax.set_title("Churn Probability Distribution")
ax.set_xlabel("Churn Probability"); ax.set_ylabel("Number of Customers")
ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR,"churn_model.png"), dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart saved: outputs/charts/churn_model.png")
print("\n🎉 Churn Prediction complete!")
print("\n💡 Interview tip: 'I used Random Forest because it handles class imbalance")
print("   well with class_weight=balanced and gives interpretable feature importances.'")
