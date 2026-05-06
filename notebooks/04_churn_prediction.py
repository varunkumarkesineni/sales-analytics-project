"""
04_churn_prediction.py
────────────────────────────────────────────────────────────────────────
STEP 4: Predict customer churn using Logistic Regression + Random Forest.
  - Feature engineering from RFM + behavioural signals
  - Model training, evaluation (accuracy, AUC, classification report)
  - Feature importance chart
  - Churn probability for every customer
  - High-risk customer list for the dashboard

Run: python 04_churn_prediction.py
Output: outputs/churn_predictions.csv, outputs/04_model_report.txt
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing   import StandardScaler
from sklearn.linear_model    import LogisticRegression
from sklearn.ensemble        import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics         import (classification_report, roc_auc_score,
                                     accuracy_score, confusion_matrix)
from sklearn.pipeline        import Pipeline

BASE  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(BASE, "data", "orders_clean.csv")
RFM   = os.path.join(BASE, "outputs", "rfm_segments.csv")
OUT   = os.path.join(BASE, "outputs")

print("=" * 60)
print("  STEP 4 — CHURN PREDICTION (ML)")
print("=" * 60)

# ── Load data ────────────────────────────────────────────────────────────
df  = pd.read_csv(CLEAN, parse_dates=["order_date"])
rfm = pd.read_csv(RFM)

snapshot = df["order_date"].max() + pd.Timedelta(days=1)

# ── Feature engineering per customer ────────────────────────────────────
features = df.groupby("customer_id").agg(
    recency        = ("order_date",    lambda x: (snapshot - x.max()).days),
    frequency      = ("order_id",      "count"),
    monetary       = ("revenue",       "sum"),
    avg_order_val  = ("revenue",       "mean"),
    total_returns  = ("is_returned",   "sum"),
    avg_rating     = ("rating",        "mean"),
    unique_cats    = ("category",      "nunique"),
    days_active    = ("order_date",    lambda x: (x.max() - x.min()).days + 1),
    last_90d_orders= ("order_date",    lambda x: (x > snapshot - pd.Timedelta(days=90)).sum()),
).reset_index()

features["return_rate"]    = (features["total_returns"] / features["frequency"]).round(4)
features["orders_per_day"] = (features["frequency"] / features["days_active"].clip(lower=1)).round(6)
features["high_value"]     = (features["monetary"] > features["monetary"].quantile(0.75)).astype(int)

# ── Define churn label ───────────────────────────────────────────────────
# Churn = inactive for > 90 days AND fewer than 2 orders in last 90 days
features["churned"] = (
    (features["recency"] > 90) & (features["last_90d_orders"] < 2)
).astype(int)

churn_rate = features["churned"].mean()
print(f"\n  Churn rate in dataset: {churn_rate*100:.1f}%")
print(f"  Churned customers    : {features['churned'].sum():,}")
print(f"  Active customers     : {(features['churned']==0).sum():,}\n")

# ── Prepare X, y ────────────────────────────────────────────────────────
feature_cols = ["recency","frequency","monetary","avg_order_val","total_returns",
                "avg_rating","unique_cats","days_active","last_90d_orders",
                "return_rate","orders_per_day","high_value"]
X = features[feature_cols]
y = features["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Model 1: Logistic Regression ─────────────────────────────────────────
print("─" * 40)
print("  Model 1: Logistic Regression")
lr_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"))
])
lr_pipe.fit(X_train, y_train)
lr_pred  = lr_pipe.predict(X_test)
lr_proba = lr_pipe.predict_proba(X_test)[:, 1]
lr_auc   = roc_auc_score(y_test, lr_proba)
lr_acc   = accuracy_score(y_test, lr_pred)
print(f"  Accuracy : {lr_acc*100:.1f}%")
print(f"  AUC-ROC  : {lr_auc:.4f}")

# ── Model 2: Random Forest ───────────────────────────────────────────────
print("\n  Model 2: Random Forest")
rf = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42,
                             class_weight="balanced", n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred  = rf.predict(X_test)
rf_proba = rf.predict_proba(X_test)[:, 1]
rf_auc   = roc_auc_score(y_test, rf_proba)
rf_acc   = accuracy_score(y_test, rf_pred)
print(f"  Accuracy : {rf_acc*100:.1f}%")
print(f"  AUC-ROC  : {rf_auc:.4f}")

# ── Model 3: Gradient Boosting ───────────────────────────────────────────
print("\n  Model 3: Gradient Boosting")
gb = GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=4, random_state=42)
gb.fit(X_train, y_train)
gb_pred  = gb.predict(X_test)
gb_proba = gb.predict_proba(X_test)[:, 1]
gb_auc   = roc_auc_score(y_test, gb_proba)
gb_acc   = accuracy_score(y_test, gb_pred)
print(f"  Accuracy : {gb_acc*100:.1f}%")
print(f"  AUC-ROC  : {gb_auc:.4f}")

# ── Best model ───────────────────────────────────────────────────────────
best_auc   = max(lr_auc, rf_auc, gb_auc)
best_name  = ["Logistic Regression","Random Forest","Gradient Boosting"][[lr_auc,rf_auc,gb_auc].index(best_auc)]
best_model = [lr_pipe, rf, gb][[lr_auc,rf_auc,gb_auc].index(best_auc)]
best_proba_all = best_model.predict_proba(X)[:, 1]
print(f"\n🏆  Best model: {best_name} (AUC = {best_auc:.4f})")

# ── Feature importance (Random Forest) ──────────────────────────────────
importance = pd.DataFrame({
    "Feature":    feature_cols,
    "Importance": rf.feature_importances_
}).sort_values("Importance", ascending=False)
print(f"\n  Top features (Random Forest):")
for _, row in importance.head(6).iterrows():
    bar = "█" * int(row["Importance"] * 100)
    print(f"    {row['Feature']:20s} {row['Importance']:.4f}  {bar}")

# ── Churn predictions for all customers ─────────────────────────────────
features["churn_probability"]  = best_proba_all.round(4)
features["churn_risk"]         = pd.cut(
    features["churn_probability"],
    bins=[0, 0.3, 0.6, 1.01],
    labels=["Low", "Medium", "High"]
)
# Merge segment info
if os.path.exists(RFM):
    seg = pd.read_csv(RFM)[["customer_id","Segment","Monetary"]]
    features = features.merge(seg, on="customer_id", how="left")

features.to_csv(os.path.join(OUT, "churn_predictions.csv"), index=False)
print(f"\n✅  Churn predictions saved → outputs/churn_predictions.csv")

high_risk = features[features["churn_risk"] == "High"].sort_values("monetary", ascending=False)
print(f"  High-risk customers: {len(high_risk):,}")

# ── Report ───────────────────────────────────────────────────────────────
report = f"""
CHURN PREDICTION MODEL REPORT
==============================
Dataset         : {len(features):,} customers
Churn rate      : {churn_rate*100:.1f}%
Train/Test split: 80/20 stratified

MODEL PERFORMANCE
-----------------
                      Accuracy   AUC-ROC
Logistic Regression : {lr_acc*100:.1f}%      {lr_auc:.4f}
Random Forest       : {rf_acc*100:.1f}%      {rf_auc:.4f}
Gradient Boosting   : {gb_acc*100:.1f}%      {gb_auc:.4f}

Best Model          : {best_name}

CLASSIFICATION REPORT (Best Model on Test Set)
-----------------------------------------------
{classification_report(y_test, best_model.predict(X_test))}

FEATURE IMPORTANCE (Random Forest)
------------------------------------
{importance.to_string(index=False)}

RISK DISTRIBUTION
-----------------
{features['churn_risk'].value_counts().to_string()}

HIGH-RISK CUSTOMERS (top 10 by monetary value)
-----------------------------------------------
{high_risk[['customer_id','monetary','churn_probability','Segment']].head(10).to_string(index=False)}
"""
with open(os.path.join(OUT, "04_model_report.txt"), "w") as f:
    f.write(report)

print("✅  Model report saved → outputs/04_model_report.txt")
print("\n" + "=" * 60)
print("  STEP 4 COMPLETE ✅")
print("=" * 60)
