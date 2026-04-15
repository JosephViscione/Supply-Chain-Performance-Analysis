USE supply_chain;

-- Query 1: Revenue and Profit by Product Category

SELECT 
    c.category_name,
    COUNT(oi.order_item_id) AS total_orders,
    SUM(oi.sales) AS total_revenue,
    SUM(oi.order_profit_per_order) AS total_profit,
    ROUND(SUM(oi.order_profit_per_order) / SUM(oi.sales) * 100, 2) AS profit_margin_pct
FROM order_items oi
JOIN products p ON oi.product_card_id = p.product_card_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_revenue DESC;

-- Query 2: Revenue and Delivery Performance by Shipping Mode
SELECT 
    o.shipping_mode,
    COUNT(oi.order_item_id) AS total_orders,
    SUM(oi.sales) AS total_revenue,
    ROUND(AVG(oi.days_for_shipping_real), 2) AS avg_actual_days,
    ROUND(AVG(oi.days_for_shipment_scheduled), 2) AS avg_scheduled_days,
    ROUND(SUM(oi.late_delivery_risk) / COUNT(oi.order_item_id) * 100, 2) AS late_delivery_pct
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
GROUP BY o.shipping_mode
ORDER BY total_revenue DESC;

-- Query 3: Revenue by Market and Region

SELECT 
    o.market,
    o.order_region,
    COUNT(oi.order_item_id) AS total_orders,
    SUM(oi.sales) AS total_revenue,
    SUM(oi.order_profit_per_order) AS total_profit,
    ROUND(SUM(oi.order_profit_per_order) / SUM(oi.sales) * 100, 2) AS profit_margin_pct
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
GROUP BY o.market, o.order_region
ORDER BY total_revenue DESC;

-- Query 4: Revenue by Customer Segment

SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(oi.order_item_id) AS total_orders,
    SUM(oi.sales) AS total_revenue,
    SUM(oi.order_profit_per_order) AS total_profit,
    ROUND(SUM(oi.sales) / COUNT(DISTINCT c.customer_id), 2) AS avg_revenue_per_customer
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.order_customer_id = c.customer_id
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;

-- Query 5: Monthly Revenue Trend

SELECT 
    YEAR(o.order_date_dateorders) AS order_year,
    MONTH(o.order_date_dateorders) AS order_month,
    COUNT(oi.order_item_id) AS total_orders,
    SUM(oi.sales) AS total_revenue,
    SUM(oi.order_profit_per_order) AS total_profit
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

-- Query 6: Top 10 Products by Revenue

SELECT 
    p.product_name,
    c.category_name,
    COUNT(oi.order_item_id) AS total_orders,
    SUM(oi.order_item_quantity) AS total_units_sold,
    SUM(oi.sales) AS total_revenue,
    SUM(oi.order_profit_per_order) AS total_profit,
    ROUND(SUM(oi.order_profit_per_order) / SUM(oi.sales) * 100, 2) AS profit_margin_pct
FROM order_items oi
JOIN products p ON oi.product_card_id = p.product_card_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY p.product_name, c.category_name
ORDER BY total_revenue DESC
LIMIT 10;