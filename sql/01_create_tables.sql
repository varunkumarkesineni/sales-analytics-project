-- ============================================================
-- STEP 1: Create Star Schema Tables
-- ============================================================
-- Run in PostgreSQL:
--   psql -U postgres -d sales_db -f sql/01_create_tables.sql
-- Or use SQLite with DB Browser for SQLite (free, download at sqlitebrowser.org)
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id      VARCHAR(20) PRIMARY KEY,
    country          VARCHAR(50),
    region           VARCHAR(50),
    first_order_date DATE,
    customer_segment VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id   VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(200),
    category     VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key    DATE PRIMARY KEY,
    day_of_week VARCHAR(10),
    month_num   INT,
    month_name  VARCHAR(10),
    quarter     VARCHAR(5),
    year        INT,
    is_weekend  BOOLEAN
);

CREATE TABLE IF NOT EXISTS fact_orders (
    order_id      VARCHAR(30),
    customer_id   VARCHAR(20),
    product_id    VARCHAR(20),
    order_date    DATE,
    quantity      INT,
    unit_price    DECIMAL(10,2),
    revenue       DECIMAL(12,2),
    cost          DECIMAL(12,2),
    profit        DECIMAL(12,2),
    profit_margin DECIMAL(5,2),
    PRIMARY KEY (order_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_orders_date     ON fact_orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON fact_orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_product  ON fact_orders(product_id);

SELECT 'Tables created successfully!' AS status;
