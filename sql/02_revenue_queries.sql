-- ============================================================
-- STEP 2: Revenue & Growth Queries
-- ============================================================
-- These are the exact queries interviewers ask you to write.
-- ============================================================

-- 1. Monthly revenue, profit, and MoM growth
SELECT
    DATE_TRUNC('month', order_date)       AS month,
    SUM(revenue)                          AS total_revenue,
    SUM(profit)                           AS total_profit,
    COUNT(DISTINCT order_id)              AS total_orders,
    COUNT(DISTINCT customer_id)           AS unique_customers,
    ROUND(SUM(profit)/SUM(revenue)*100,1) AS margin_pct,
    ROUND(SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY DATE_TRUNC('month',order_date)), 2) AS revenue_change,
    ROUND(
        (SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY DATE_TRUNC('month',order_date)))
        / NULLIF(LAG(SUM(revenue)) OVER (ORDER BY DATE_TRUNC('month',order_date)), 0) * 100
    , 1) AS mom_growth_pct
FROM fact_orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- ─────────────────────────────────────────────────────────────

-- 2. Quarterly revenue summary
SELECT
    EXTRACT(YEAR  FROM order_date) AS year,
    EXTRACT(QUARTER FROM order_date) AS quarter,
    SUM(revenue)   AS quarterly_revenue,
    SUM(profit)    AS quarterly_profit,
    COUNT(DISTINCT customer_id) AS customers
FROM fact_orders
GROUP BY 1, 2
ORDER BY 1, 2;

-- ─────────────────────────────────────────────────────────────

-- 3. Revenue by region
SELECT
    c.region,
    SUM(o.revenue)                            AS total_revenue,
    SUM(o.profit)                             AS total_profit,
    ROUND(SUM(o.profit)/SUM(o.revenue)*100,1) AS margin_pct,
    COUNT(DISTINCT o.customer_id)             AS customers,
    COUNT(DISTINCT o.order_id)                AS orders
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;

-- ─────────────────────────────────────────────────────────────

-- 4. Running total revenue (cumulative)
SELECT
    order_date,
    revenue,
    SUM(revenue) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS cumulative_revenue
FROM fact_orders
ORDER BY order_date;
