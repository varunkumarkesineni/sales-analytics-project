-- ============================================================
-- STEP 4: Product & Category Analysis Queries
-- ============================================================

-- 1. Top 10 products by revenue and profit
SELECT
    p.product_name,
    p.category,
    COUNT(DISTINCT o.order_id)                AS total_orders,
    SUM(o.quantity)                           AS units_sold,
    ROUND(SUM(o.revenue),2)                   AS revenue,
    ROUND(SUM(o.profit),2)                    AS profit,
    ROUND(SUM(o.profit)/SUM(o.revenue)*100,1) AS margin_pct,
    RANK() OVER (ORDER BY SUM(o.profit) DESC) AS profit_rank
FROM fact_orders o
JOIN dim_products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- ─────────────────────────────────────────────────────────────

-- 2. Category performance summary
SELECT
    p.category,
    COUNT(DISTINCT o.order_id)                AS orders,
    SUM(o.revenue)                            AS revenue,
    SUM(o.profit)                             AS profit,
    ROUND(SUM(o.profit)/SUM(o.revenue)*100,1) AS margin_pct,
    ROUND(AVG(o.revenue),2)                   AS avg_order_value,
    ROUND(SUM(o.revenue) * 100.0 / SUM(SUM(o.revenue)) OVER (), 1) AS revenue_share_pct
FROM fact_orders o
JOIN dim_products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- ─────────────────────────────────────────────────────────────

-- 3. Month-over-month product growth (window function)
WITH monthly_product AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        p.product_name,
        SUM(o.revenue) AS revenue
    FROM fact_orders o
    JOIN dim_products p ON o.product_id = p.product_id
    GROUP BY 1, 2
)
SELECT *,
    revenue - LAG(revenue) OVER (PARTITION BY product_name ORDER BY month) AS revenue_change,
    ROUND(
        (revenue - LAG(revenue) OVER (PARTITION BY product_name ORDER BY month))
        / NULLIF(LAG(revenue) OVER (PARTITION BY product_name ORDER BY month), 0) * 100
    ,1) AS mom_growth_pct
FROM monthly_product
ORDER BY product_name, month;

-- ─────────────────────────────────────────────────────────────

-- 4. Average order value by category (for dashboard KPI)
SELECT
    p.category,
    ROUND(AVG(order_totals.order_revenue),2) AS avg_order_value
FROM (
    SELECT order_id, product_id, SUM(revenue) AS order_revenue
    FROM fact_orders
    GROUP BY order_id, product_id
) order_totals
JOIN dim_products p ON order_totals.product_id = p.product_id
GROUP BY p.category
ORDER BY avg_order_value DESC;
