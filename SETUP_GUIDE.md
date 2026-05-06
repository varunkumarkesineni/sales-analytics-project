# 🚀 SETUP GUIDE — Run This Project in 10 Minutes

This guide will help you set up and execute the complete **Sales & E-Commerce Analytics System** from scratch.

---

# 📋 Prerequisites

Before starting, ensure the following are installed:

- Python 3.10+  
  https://python.org/downloads

- pip (comes with Python)

- VS Code (Recommended IDE)  
  https://code.visualstudio.com

---

# ⚙️ STEP 1 — Install Project Dependencies

Open terminal inside the project folder and run:

```bash
pip install -r requirements.txt
```

This installs all required libraries including:

- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- SQLAlchemy
- Plotly
- OpenPyXL

---

# 📦 STEP 2 — Add Dataset

You have 2 options:

---

## ✅ Option A — Auto-Generated Sample Dataset (Easiest)

No download required.

If no dataset is found inside:

```bash
data/raw/
```

the project automatically generates **10,000+ sample transaction rows** for testing and demo purposes.

Perfect for:
- Quick execution
- Practice
- Portfolio setup
- Learning pipeline flow

---

## ✅ Option B — Real Kaggle Dataset (Recommended)

### Dataset:
UK Online Retail Dataset

🔗 https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci

### Steps:
1. Download:
   ```text
   online_retail_II.xlsx
   ```

2. Place the file inside:

```bash
data/raw/
```

This option is recommended for:
- Resume projects
- Placement interviews
- Real-world analysis demonstrations

---

# ▶️ STEP 3 — Run the Complete Analytics Pipeline

## Run Everything Automatically

```bash
python notebooks/run_all.py
```

This executes the entire pipeline:

1. Data Cleaning
2. KPI Analysis
3. RFM Segmentation
4. Cohort Analysis
5. Churn Prediction

---

# 🧩 Run Individual Modules (Optional)

## 1️⃣ Data Cleaning

```bash
python notebooks/01_data_cleaning.py
```

### Tasks:
- Missing value handling
- Duplicate removal
- Date formatting
- Revenue calculations

---

## 2️⃣ KPI Analysis

```bash
python notebooks/02_kpi_analysis.py
```

### Generates:
- Revenue trends
- KPI reports
- Business charts

---

## 3️⃣ RFM Customer Segmentation

```bash
python notebooks/03_rfm_segmentation.py
```

### Identifies:
- VIP customers
- Loyal customers
- Lost customers
- High-value segments

---

## 4️⃣ Cohort Retention Analysis

```bash
python notebooks/04_cohort_analysis.py
```

### Generates:
- Retention matrix
- Customer retention heatmaps

---

## 5️⃣ Churn Prediction (Machine Learning)

```bash
python notebooks/05_churn_prediction.py
```

### ML Model:
- Random Forest Classifier

### Predicts:
- Customers likely to churn
- High-risk customer segments

---

# 📊 STEP 4 — View Generated Outputs

After execution, open:

```bash
outputs/
```

You should see:

```bash
outputs/
├── kpi_summary.csv
├── kpi_monthly.csv
├── rfm_segments.csv
├── rfm_segment_summary.csv
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

# 📈 Understanding the Outputs

| File | Description |
|---|---|
| `kpi_summary.csv` | Overall business KPIs |
| `kpi_monthly.csv` | Month-wise performance |
| `rfm_segments.csv` | Customer segmentation |
| `cohort_table.csv` | Retention metrics |
| `churn_predictions.csv` | ML churn predictions |

---

# 🗄️ STEP 5 — SQL Database Setup (Optional but Recommended)

---

## Option A — SQLite (Recommended for Beginners)

### Step 1
Download:

https://sqlitebrowser.org

### Step 2
Create database:

```text
sales_db.sqlite
```

### Step 3
Open:

```text
Execute SQL
```

### Step 4
Run SQL files from:

```bash
sql/
```

in this order:

```text
01_create_tables.sql
02_revenue_queries.sql
03_customer_queries.sql
04_product_queries.sql
```

---

## Option B — PostgreSQL

### Create Database

```bash
psql -U postgres -c "CREATE DATABASE sales_db;"
```

### Execute SQL Files

```bash
psql -U postgres -d sales_db -f sql/01_create_tables.sql
psql -U postgres -d sales_db -f sql/02_revenue_queries.sql
psql -U postgres -d sales_db -f sql/03_customer_queries.sql
psql -U postgres -d sales_db -f sql/04_product_queries.sql
```

---

# 📊 STEP 6 — Build Dashboard

Follow:

```bash
dashboard/dashboard_guide.md
```

Recommended tools:

| Tool | Link |
|---|---|
| Power BI Desktop | https://powerbi.microsoft.com/desktop |
| Tableau Public | https://public.tableau.com |

---

## Dashboard Features

Recommended dashboard pages:

- KPI Overview
- Revenue Trends
- Customer Segmentation
- Retention Analysis
- Churn Prediction

---

# 🌐 STEP 7 — Upload Project to GitHub

Initialize Git repository:

```bash
git init
git add .
git commit -m "Initial commit: Sales Analytics Project"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/sales-analytics-project.git
git push -u origin main
```

Replace:

```text
YOURUSERNAME
```

with your actual GitHub username.

---

# 💼 STEP 8 — Add Project to LinkedIn

Use resources from:

```bash
docs/linkedin_post.md
docs/resume_bullets.md
```

Recommended additions:
- Dashboard screenshots
- GitHub repository link
- Project KPIs
- Skills used

---

# 🧠 Interview Talking Points

Example explanation:

> “I built an end-to-end sales analytics system using Python, SQL, Machine Learning, and Power BI. The project involved data cleaning, KPI analysis, customer segmentation using RFM analysis, cohort retention analysis, and churn prediction using Random Forest. Finally, I created interactive dashboards to visualize business insights.”

---

# ❗ Troubleshooting

| Error | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `FileNotFoundError` | Ensure terminal is opened in project root folder |
| `No data in raw/` | Scripts auto-generate sample data automatically |
| `sklearn not found` | Run `pip install scikit-learn` |
| `python not recognized` | Reinstall Python and enable “Add Python to PATH” |
| Charts not generated | Ensure `outputs/charts/` folder exists |

---

# ✅ Expected Final Outcome

After completing setup successfully, you will have:

- Cleaned business dataset
- KPI reports
- Customer segmentation analysis
- Retention heatmaps
- Churn prediction model
- Power BI dashboard
- GitHub-ready portfolio project
- LinkedIn-ready analytics showcase

---

# 🚀 You're Ready

This project demonstrates real-world skills in:

```text
Python
SQL
Machine Learning
Power BI
Data Analytics
Business Intelligence
Customer Analytics
Data Visualization
Git & GitHub
```

Good luck building your analytics portfolio 🚀
```
