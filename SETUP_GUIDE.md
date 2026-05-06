# 🚀 SETUP GUIDE — Run This Project in 10 Minutes

## Prerequisites
- Python 3.8+ installed (https://python.org)
- pip installed

---

## STEP 1 — Install Python dependencies

Open terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

---

## STEP 2 — Get the dataset (2 options)

### Option A: Use sample data (easiest — no download needed)
Just skip this step. The scripts auto-generate 10,000 sample rows if no file is found.

### Option B: Real Kaggle data (recommended for interviews)
1. Go to: https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci
2. Download `online_retail_II.xlsx`
3. Place it in: `data/raw/` folder

---

## STEP 3 — Run the full pipeline

### Run everything at once:
```bash
python notebooks/run_all.py
```

### Or run step by step:
```bash
python notebooks/01_data_cleaning.py     # Clean raw data
python notebooks/02_kpi_analysis.py      # Calculate KPIs + charts
python notebooks/03_rfm_segmentation.py  # Customer segments
python notebooks/04_cohort_analysis.py   # Retention heatmap
python notebooks/05_churn_prediction.py  # ML churn model
```

---

## STEP 4 — View your outputs

After running, check these folders:
```
outputs/
├── kpi_summary.csv          ← Overall KPIs
├── kpi_monthly.csv          ← Month-by-month data
├── rfm_segments.csv         ← Customer segments
├── rfm_segment_summary.csv  ← Segment comparison
├── cohort_table.csv         ← Retention % table
├── churn_predictions.csv    ← Churn scores per customer
└── charts/
    ├── kpi_dashboard.png    ← 4-chart KPI overview
    ├── category_breakdown.png
    ├── rfm_segmentation.png ← 3-chart RFM view
    ├── cohort_heatmap.png   ← THE KEY CHART
    └── churn_model.png      ← ML model results
```

---

## STEP 5 — Set up SQL (optional but recommended)

### Using SQLite (easiest, no installation):
1. Download DB Browser for SQLite: https://sqlitebrowser.org
2. Create new database: `sales_db.sqlite`
3. Go to Execute SQL tab
4. Paste and run files from the `sql/` folder in order (01 → 04)

### Using PostgreSQL:
```bash
psql -U postgres -c "CREATE DATABASE sales_db;"
psql -U postgres -d sales_db -f sql/01_create_tables.sql
psql -U postgres -d sales_db -f sql/02_revenue_queries.sql
psql -U postgres -d sales_db -f sql/03_customer_queries.sql
psql -U postgres -d sales_db -f sql/04_product_queries.sql
```

---

## STEP 6 — Build Dashboard

Follow: `dashboard/dashboard_guide.md`

Free tools:
- Power BI Desktop: https://powerbi.microsoft.com/desktop
- Tableau Public:   https://public.tableau.com

Load the CSVs from `outputs/` folder into Power BI/Tableau.

---

## STEP 7 — Upload to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Sales Analytics Project"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/sales-analytics-project.git
git push -u origin main
```

---

## STEP 8 — Add to LinkedIn

Copy from: `docs/linkedin_post.md`
Copy resume bullets from: `docs/resume_bullets.md`

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `FileNotFoundError` | Make sure you're running from the project root folder |
| `No data in raw/` | Scripts use sample data automatically — this is fine |
| `sklearn not found` | Run `pip install scikit-learn` |

