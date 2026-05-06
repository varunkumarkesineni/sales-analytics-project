# 🚀 Sales & E-Commerce Analytics System

> End-to-End Business Analytics Project using Python, SQL, Machine Learning, and Power BI/Tableau

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![SQL](https://img.shields.io/badge/SQL-Analytics-orange?style=for-the-badge&logo=mysql)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?style=for-the-badge&logo=powerbi)
![MachineLearning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-green?style=for-the-badge)

---

# 📌 Project Overview

The **Sales & E-Commerce Analytics System** is an industry-style end-to-end analytics project designed to simulate real-world business intelligence workflows used by modern e-commerce companies.

This project transforms raw transactional data into actionable business insights through:

- Data Cleaning & Preprocessing
- KPI & Revenue Analysis
- Customer Segmentation (RFM)
- Cohort Retention Analysis
- Churn Prediction using Machine Learning
- Interactive Dashboard Development
- SQL-Based Business Analysis

The final output includes business reports, analytical visualizations, predictive modeling, and Power BI/Tableau dashboards.

---

# 🏢 Business Problem

A mid-sized e-commerce company wants to:

- Understand sales performance
- Identify high-value customers
- Improve customer retention
- Detect churn risks
- Optimize product strategy
- Track KPIs through dashboards

This project builds a complete analytics pipeline to solve these business challenges using Python, SQL, and BI tools.

---

# 🗂️ Project Structure

```bash
sales_analytics_project/
│
├── data/
│   ├── raw/                  # Raw datasets
│   └── cleaned/              # Cleaned datasets
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
│   └── dashboard_guide.md
│
├── outputs/
│   ├── charts/
│   └── generated CSV reports
│
├── docs/
│   ├── linkedin_post.md
│   └── resume_bullets.md
│
├── requirements.txt
├── README.md
└── SETUP_GUIDE.md
```

---

# 🔧 Tech Stack

| Category | Tools & Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn |
| Database | PostgreSQL / SQLite |
| Dashboard | Power BI / Tableau |
| Version Control | Git & GitHub |

---

# 📦 Dataset

## Recommended Dataset — UK Online Retail Dataset

🔗 https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci

### Dataset Includes:
- Customer transactions
- Product information
- Invoice data
- Revenue metrics
- Purchase timestamps

### Setup:
Download:

```text
online_retail_II.xlsx
```

Place inside:

```bash
data/raw/
```

---

# ⚙️ Installation & Setup

## Step 1 — Clone Repository

```bash
git clone https://github.com/varunkumarkesineni/sales-analytics-project.git
cd sales-analytics-project
```

---

## Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3 — Add Dataset

Place dataset file(s) inside:

```bash
data/raw/
```

---

## Step 4 — Run Complete Pipeline

```bash
python notebooks/run_all.py
```

---

## Step 5 — Run Individual Modules (Optional)

```bash
python notebooks/01_data_cleaning.py
python notebooks/02_kpi_analysis.py
python notebooks/03_rfm_segmentation.py
python notebooks/04_cohort_analysis.py
python notebooks/05_churn_prediction.py
```

---

# 📊 Core Analytics Modules

## 1️⃣ Data Cleaning & Preprocessing

### Tasks Performed:
- Missing value handling
- Duplicate removal
- Date formatting
- Revenue calculations
- Data transformation

### Tools Used:
- Pandas
- NumPy

---

## 2️⃣ KPI & Revenue Analysis

### KPIs Generated:
- Total Revenue
- Monthly Revenue Trends
- Order Volume
- Customer Growth
- Product Performance

### Outputs:
- `kpi_summary.csv`
- `kpi_monthly.csv`

---

## 3️⃣ Customer Segmentation (RFM Analysis)

RFM segmentation categorizes customers using:

| Metric | Description |
|---|---|
| Recency | Last purchase timing |
| Frequency | Purchase frequency |
| Monetary | Total customer spend |

### Business Impact:
- Identifies loyal customers
- Detects inactive users
- Supports targeted marketing campaigns

### Outputs:
- `rfm_segments.csv`
- `rfm_segment_summary.csv`

---

## 4️⃣ Cohort Retention Analysis

Cohort analysis tracks customer retention patterns over time.

### Key Insights:
- Repeat purchase behavior
- Monthly retention trends
- Churn movement across cohorts

### Outputs:
- `cohort_table.csv`
- Retention heatmaps

---

## 5️⃣ Churn Prediction using Machine Learning

This module predicts customers likely to stop purchasing.

### ML Model Used:
- Random Forest Classifier

### Features Used:
- Purchase frequency
- Recency
- Revenue contribution
- Behavioral metrics

### Outputs:
- `churn_predictions.csv`
- ML performance charts

---

# 📈 Dashboard Features

The Power BI / Tableau dashboard includes:

- Executive KPI Overview
- Monthly Revenue Trends
- Customer Segmentation
- Retention Heatmaps
- Churn Risk Analysis
- Interactive Filters & Slicers

---

# 📁 Generated Outputs

After successful execution:

```bash
outputs/
│
├── kpi_summary.csv
├── kpi_monthly.csv
├── rfm_segments.csv
├── cohort_table.csv
├── churn_predictions.csv
│
└── charts/
    ├── kpi_dashboard.png
    ├── category_breakdown.png
    ├── rfm_segmentation.png
    ├── cohort_heatmap.png
    └── churn_model.png
```

---

# 📊 Sample Business Insights

- Top 20% of customers generated nearly 68% of total revenue
- Customer retention declined from Q1 to Q4
- High-value customers were identified using RFM analysis
- Churn-prone customers were predicted using Machine Learning
- KPI dashboards improved business monitoring and decision-making

---

# 🧠 Skills Demonstrated

```text
Python
SQL
Pandas
NumPy
Scikit-learn
Machine Learning
Power BI
Tableau
Data Visualization
RFM Analysis
Cohort Analysis
Business Intelligence
Customer Analytics
KPI Reporting
Git & GitHub
```

---

# 📷 Dashboard Preview

> Add your Power BI/Tableau screenshots here.

Example:

```md
![Dashboard](outputs/charts/dashboard1.png)
```

---

# 🚀 Future Enhancements

- Real-time dashboard integration
- Cloud deployment using AWS/Azure
- Advanced forecasting models
- Recommendation systems
- Streamlit web application deployment

---

# 👨‍💻 Author

## Varun Kumar Kesineni

### 🔗 LinkedIn
https://www.linkedin.com/in/varun-kumar-kesineni-80a427326/

### 🔗 GitHub
https://github.com/varunkumarkesineni

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful:

- Star ⭐ this repository
- Connect with me on LinkedIn
- Fork this project for learning

```
