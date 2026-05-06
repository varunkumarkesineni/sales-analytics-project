-- ============================================================
-- STEP 3: Customer Analysis Queries
-- ============================================================

-- 1. RFM Segmentation in pure SQL
WITH rfm_raw AS (
    SELECT
        customer_id,
        MAX(order_date)                          AS last_order,
        COUNT(DISTINCT order_id)                 AS frequency,
        SUM(revenue)                             AS monetary,
        CURRENT_DATE - MAX(order_date)           AS recency_days
    FROM fact_orders
    GROUP BY customer_id
),
rfm_scored AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency_days ASC)  AS r_score,
        NTILE(5) OVER (ORDER BY frequency DESC)    AS f_score,
        NTILE(5) OVER (ORDER BY monetary DESC)     AS m_score
    FROM rfm_raw
)
SELECT
    customer_id, last_order, frequency, monetary, recency_days,
    r_score, f_score, m_score,
    r_score + f_score + m_score AS rfm_total,
    CASE
        WHEN r_score + f_score + m_score >= 12 THEN 'Champions'
        WHEN r_score + f_score + m_score >= 9  THEN 'Loyal'
        WHEN r_score + f_score + m_score >= 6  THEN 'At Risk'
        ELSE 'Lost'
    END AS customer_segment
FROM rfm_scored
ORDER BY rfm_total DESC;

-- ─────────────────────────────────────────────────────────────

-- 2. Customer Lifetime Value (CLV)
SELECT
    customer_id,
    COUNT(DISTINCT order_id)     AS total_orders,
    SUM(revenue)                 AS total_revenue,
    AVG(revenue)                 AS avg_order_value,
    MIN(order_date)              AS first_order,
    MAX(order_date)              AS last_order,
    MAX(order_date) - MIN(order_date) AS customer_lifespan_days,
    ROUND(
        (SUM(revenue) / NULLIF(COUNT(DISTINCT order_id),0)) *
        (COUNT(DISTINCT order_id) / NULLIF(EXTRACT(DAY FROM MAX(order_date)-MIN(order_date))/365.0, 0))
    , 2) AS estimated_clv
FROM fact_orders
GROUP BY customer_id
ORDER BY estimated_clv DESC
LIMIT 20;

-- ─────────────────────────────────────────────────────────────

-- 3. Cohort retention table
WITH cohorts AS (
    SELECT customer_id,
           DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM fact_orders GROUP BY 1
),
orders_with_cohort AS (
    SELECT o.customer_id, c.cohort_month,
           DATE_TRUNC('month', o.order_date) AS order_month,
           EXTRACT(YEAR  FROM AGE(DATE_TRUNC('month',o.order_date), c.cohort_month))*12 +
           EXTRACT(MONTH FROM AGE(DATE_TRUNC('month',o.order_date), c.cohort_month)) AS month_num
    FROM fact_orders o JOIN cohorts c USING (customer_id)
)
SELECT
    TO_CHAR(cohort_month,'YYYY-MM') AS cohort,
    month_num,
    COUNT(DISTINCT customer_id) AS customers
FROM orders_with_cohort
GROUP BY 1, 2
ORDER BY 1, 2;

-- ─────────────────────────────────────────────────────────────

-- 4. New vs Returning customers per month
WITH first_orders AS (
    SELECT customer_id, MIN(order_date) AS first_date FROM fact_orders GROUP BY 1
)
SELECT
    DATE_TRUNC('month', o.order_date) AS month,
    COUNT(DISTINCT CASE WHEN o.order_date = f.first_date THEN o.customer_id END) AS new_customers,
    COUNT(DISTINCT CASE WHEN o.order_date > f.first_date  THEN o.customer_id END) AS returning_customers
FROM fact_orders o
JOIN first_orders f USING (customer_id)
GROUP BY 1 ORDER BY 1;
