# Dashboard Build Guide — Power BI / Tableau

## Option A: Power BI (Recommended for placements)

### Setup
1. Download Power BI Desktop FREE: https://powerbi.microsoft.com/desktop
2. Open Power BI → Get Data → Text/CSV
3. Load: outputs/kpi_monthly.csv, outputs/rfm_segments.csv, outputs/churn_predictions.csv

### Page 1 — Executive Summary
- KPI Cards: Total Revenue, Total Profit, Total Orders, Avg Order Value
- Line Chart: Monthly Revenue Trend (x=month, y=revenue)
- Donut Chart: Revenue by Category
- Slicer: Date Range, Region, Category

### Page 2 — Customer Analysis
- Table: RFM Segments with customer counts
- Bar Chart: Revenue by Segment
- Scatter: Recency vs Monetary (colored by segment)
- KPI Card: Churn Risk % (High Risk customers)

### Page 3 — Product Analysis
- Bar Chart: Top 10 Products by Revenue
- Matrix: Category × Quarter revenue grid
- Line Chart: Profit Margin % trend by month

### Page 4 — Churn Dashboard
- Gauge: Overall Churn Rate %
- Bar Chart: Customers by Risk Level (Low/Medium/High)
- Table: Top 20 High-Risk Customers (customer_id, revenue, churn_probability)
- Line Chart: Churn Rate trend over months

---

## Option B: Tableau Public (Free, shareable link)

1. Download Tableau Public FREE: https://public.tableau.com
2. Connect → Text File → load orders_clean.csv
3. Create calculated fields:
   - Profit Margin: SUM([Profit])/SUM([Revenue])
   - Churn Flag: IF DATEDIFF('day',[Order Date],TODAY()) > 90 THEN "Churned" ELSE "Active" END

### Must-have visualizations for Tableau:
- Revenue heat map by Month × Category
- Customer map by Country/Region (if country column exists)
- Cohort retention table (use cohort_table.csv output)
- RFM scatter plot

---

## Publish & Share
- Power BI: Publish to Power BI Service (free with work/edu email)
- Tableau: Save to Tableau Public → get shareable link
- Add the link to your GitHub README and LinkedIn project

---

## Screenshot guide for LinkedIn
Take screenshots of:
1. Executive Summary page (shows KPI cards)
2. Cohort heatmap (most impressive visual)
3. RFM scatter plot
Upload all 3 to your LinkedIn project gallery.
