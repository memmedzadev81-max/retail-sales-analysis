-- ============================================================
-- Retail Sales Analysis - SQL Queries
-- Real-world style queries used by Junior Data Analysts
-- Database: retail_sales.db  |  Table: sales
-- ============================================================

-- 1. Overall KPIs
SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit_margin), 2) AS avg_profit_margin,
    ROUND(SUM(quantity), 0) AS total_units_sold
FROM sales;


-- 2. Sales & Profit by Year
SELECT
    year,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(*) AS orders
FROM sales
GROUP BY year
ORDER BY year;


-- 3. Monthly Sales Trend (for line chart)
SELECT
    year,
    month,
    month_name,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit
FROM sales
GROUP BY year, month, month_name
ORDER BY year, month;


-- 4. Sales by Region (bar chart)
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(*) AS orders,
    ROUND(AVG(profit_margin), 2) AS avg_margin
FROM sales
GROUP BY region
ORDER BY total_sales DESC;


-- 5. Category Performance
SELECT
    category,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) * 100.0 / SUM(sales), 2) AS profit_margin_pct,
    COUNT(*) AS orders
FROM sales
GROUP BY category
ORDER BY sales DESC;


-- 6. Top 10 Sub-Categories by Sales
SELECT
    sub_category,
    category,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY sub_category, category
ORDER BY sales DESC
LIMIT 10;


-- 7. Customer Segment Analysis
SELECT
    segment,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM sales
GROUP BY segment
ORDER BY sales DESC;


-- 8. Shipping Mode Performance
SELECT
    ship_mode,
    COUNT(*) AS orders,
    ROUND(AVG(days_to_ship), 1) AS avg_days_to_ship,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit
FROM sales
GROUP BY ship_mode
ORDER BY orders DESC;


-- 9. Profitability by Region & Category (heatmap style)
SELECT
    region,
    category,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) * 100.0 / NULLIF(SUM(sales), 0), 2) AS margin_pct
FROM sales
GROUP BY region, category
ORDER BY region, sales DESC;


-- 10. Top 15 most profitable products
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    SUM(quantity) AS units
FROM sales
GROUP BY product_name, category, sub_category
ORDER BY profit DESC
LIMIT 15;


-- 11. Discount impact on profit (business insight)
SELECT
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.10 THEN 'Low (1-10%)'
        WHEN discount <= 0.20 THEN 'Medium (11-20%)'
        ELSE 'High (>20%)'
    END AS discount_band,
    COUNT(*) AS orders,
    ROUND(AVG(sales), 2) AS avg_sales,
    ROUND(AVG(profit), 2) AS avg_profit,
    ROUND(AVG(profit_margin), 2) AS avg_margin
FROM sales
GROUP BY discount_band
ORDER BY 
    CASE discount_band
        WHEN 'No Discount' THEN 1
        WHEN 'Low (1-10%)' THEN 2
        WHEN 'Medium (11-20%)' THEN 3
        ELSE 4
    END;


-- 12. Year-over-Year growth (simple)
WITH yearly AS (
    SELECT year, SUM(sales) AS sales, SUM(profit) AS profit
    FROM sales
    GROUP BY year
)
SELECT
    a.year,
    ROUND(a.sales, 2) AS sales,
    ROUND(a.profit, 2) AS profit,
    ROUND((a.sales - b.sales) * 100.0 / NULLIF(b.sales, 0), 2) AS sales_growth_pct,
    ROUND((a.profit - b.profit) * 100.0 / NULLIF(b.profit, 0), 2) AS profit_growth_pct
FROM yearly a
LEFT JOIN yearly b ON a.year = b.year + 1
ORDER BY a.year;
