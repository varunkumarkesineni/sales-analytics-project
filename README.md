# 🛒 Sales & E-commerce Analytics System

> End-to-end business analytics project using Python, SQL, and Power BI / Tableau  
> Built for campus placements & data analyst internship interviews

---

## 📌 Problem Statement

A mid-size e-commerce company wants to understand its sales performance, identify high-value customers, reduce churn, and optimize product strategy. This project builds a complete analytics pipeline — from raw data to an interactive KPI dashboard.

---

## 🗂️ Project Structure

```
sales_analytics_project/
│
├── data/
│   ├── raw/                  ← Place downloaded Kaggle CSV files here
│   └── cleaned/              ← Auto-generated after running scripts
│
├── notebooks/
│   ├── 01_data_cleaning.py
│   ├── 02_kpi_analysis.py
│   ├── 03_rfm_segmentation.py
│   ├── 04_cohort_analysis.py
│   └── 05_churn_prediction.py
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_revenue_queries.sql
│   ├── 03_customer_queries.sql
│   └── 04_product_queries.sql
│
├── dashboard/
│   └── dashboard_guide.md    ← Step-by-step Power BI / Tableau instructions
│
├── outputs/
│   └── (auto-generated CSVs, charts, reports)
│
├── docs/
│   ├── linkedin_post.md
│   └── resume_bullets.md
│
├── requirements.txt
└── README.md
```

---

## 🔧 Tech Stack

| Layer | Tool |
|---|---|
| Data Cleaning | Python, Pandas, NumPy |
| Database | PostgreSQL / SQLite |
| Analysis | Python, Pandas, Scikit-learn |
| Visualization | Matplotlib, Seaborn |
| Dashboard | Power BI / Tableau Public |
| Version Control | Git + GitHub |

---

## 📦 Dataset

Download from Kaggle (free account required):

**Option A (Recommended):** UK Online Retail Dataset  
🔗 https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci  
→ Download `online_retail_II.xlsx`, convert to CSV, place in `data/raw/`

**Option B:** Brazilian E-commerce (Olist)  
🔗 https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
→ Download all CSVs, place in `data/raw/`

---

## 🚀 How to Run (Step by Step)

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Add your dataset
Place downloaded CSV(s) in `data/raw/` folder.

### Step 3 — Clean the data
```bash
python notebooks/01_data_cleaning.py
```

### Step 4 — Run KPI analysis
```bash
python notebooks/02_kpi_analysis.py
```

### Step 5 — RFM Segmentation
```bash
python notebooks/03_rfm_segmentation.py
```

### Step 6 — Cohort Analysis
```bash
python notebooks/04_cohort_analysis.py
```

### Step 7 — Churn Prediction
```bash
python notebooks/05_churn_prediction.py
```

### Step 8 — Set up SQL database
```bash
# Open PostgreSQL or use SQLite
# Run files in order:
# sql/01_create_tables.sql
# sql/02_revenue_queries.sql
# sql/03_customer_queries.sql
# sql/04_product_queries.sql
```

### Step 9 — Build Dashboard
Follow: `dashboard/dashboard_guide.md`

---

## 📊 Key Findings (Sample — replace with your real numbers)

- Top 20% of customers drove **68% of total revenue**
- Average customer retention dropped from **74% (Q1)** to **55% (Q4)**
- Electronics category had the highest margin at **26.3%**
- 18% of "At Risk" customers were successfully re-engaged via discount triggers
- Churn prediction model achieved **82% accuracy** using Random Forest

---

## 🧠 Skills Demonstrated

`Python` `Pandas` `NumPy` `Scikit-learn` `SQL` `PostgreSQL` `Power BI` `Tableau`  
`RFM Analysis` `Cohort Analysis` `Churn Prediction` `Star Schema` `Window Functions` `KPI Dashboards`

---

## 👤 Author

Your Name  
LinkedIn: https://www.linkedin.com/in/varun-kumar-kesineni-80a427326

GitHub: https://github.com/varunkumarkesineni

---

## 📄 License

MIT License — free to use and modify for your portfolio.
