-- Customer Segmentation and Lifetime Value Analysis
-- Superstore Dataset Analysis

-- 1. BASIC CUSTOMER METRICS
SELECT 
    customer_id,
    customer_name,
    segment,
    region,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(sales) as total_sales,
    SUM(profit) as total_profit,
    AVG(sales) as avg_order_value,
    MIN(order_date) as first_order_date,
    MAX(order_date) as last_order_date,
    DATEDIFF(MAX(order_date), MIN(order_date)) as customer_lifetime_days
FROM superstore
GROUP BY customer_id, customer_name, segment, region
ORDER BY total_sales DESC;

-- 2. CUSTOMER LIFETIME VALUE (CLV) CALCULATION
WITH customer_metrics AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        COUNT(DISTINCT order_id) as total_orders,
        SUM(sales) as total_sales,
        SUM(profit) as total_profit,
        AVG(sales) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        DATEDIFF(MAX(order_date), MIN(order_date)) as customer_lifetime_days
    FROM superstore
    GROUP BY customer_id, customer_name, segment, region
),
clv_calculation AS (
    SELECT 
        *,
        -- CLV = Total Profit + (Avg Order Value * Expected Future Orders)
        total_profit + (avg_order_value * 3) as estimated_clv,
        -- Customer Value Score (0-100)
        CASE 
            WHEN total_sales >= 10000 THEN 100
            WHEN total_sales >= 5000 THEN 80
            WHEN total_sales >= 2000 THEN 60
            WHEN total_sales >= 1000 THEN 40
            WHEN total_sales >= 500 THEN 20
            ELSE 10
        END as value_score
    FROM customer_metrics
)
SELECT 
    *,
    CASE 
        WHEN estimated_clv >= 5000 THEN 'VIP'
        WHEN estimated_clv >= 2000 THEN 'High Value'
        WHEN estimated_clv >= 1000 THEN 'Medium Value'
        WHEN estimated_clv >= 500 THEN 'Low Value'
        ELSE 'At Risk'
    END as customer_tier
FROM clv_calculation
ORDER BY estimated_clv DESC;

-- 3. RFM ANALYSIS (Recency, Frequency, Monetary)
WITH rfm_scores AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        -- Recency: Days since last order
        DATEDIFF(CURRENT_DATE, MAX(order_date)) as recency_days,
        -- Frequency: Number of orders
        COUNT(DISTINCT order_id) as frequency,
        -- Monetary: Total sales value
        SUM(sales) as monetary,
        -- RFM Scores (1-5, where 5 is best)
        CASE 
            WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) <= 30 THEN 5
            WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) <= 60 THEN 4
            WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) <= 90 THEN 3
            WHEN DATEDIFF(CURRENT_DATE, MAX(order_date)) <= 180 THEN 2
            ELSE 1
        END as recency_score,
        CASE 
            WHEN COUNT(DISTINCT order_id) >= 10 THEN 5
            WHEN COUNT(DISTINCT order_id) >= 7 THEN 4
            WHEN COUNT(DISTINCT order_id) >= 5 THEN 3
            WHEN COUNT(DISTINCT order_id) >= 3 THEN 2
            ELSE 1
        END as frequency_score,
        CASE 
            WHEN SUM(sales) >= 5000 THEN 5
            WHEN SUM(sales) >= 2000 THEN 4
            WHEN SUM(sales) >= 1000 THEN 3
            WHEN SUM(sales) >= 500 THEN 2
            ELSE 1
        END as monetary_score
    FROM superstore
    GROUP BY customer_id, customer_name, segment, region
),
rfm_segments AS (
    SELECT 
        *,
        (recency_score + frequency_score + monetary_score) as rfm_score,
        CASE 
            WHEN (recency_score + frequency_score + monetary_score) >= 13 THEN 'Champions'
            WHEN (recency_score + frequency_score + monetary_score) >= 11 THEN 'Loyal Customers'
            WHEN (recency_score + frequency_score + monetary_score) >= 9 THEN 'At Risk'
            WHEN (recency_score + frequency_score + monetary_score) >= 7 THEN 'Can\'t Lose Them'
            WHEN (recency_score + frequency_score + monetary_score) >= 5 THEN 'About to Sleep'
            ELSE 'Lost'
        END as rfm_segment
    FROM rfm_scores
)
SELECT 
    *,
    CASE 
        WHEN rfm_segment = 'Champions' THEN 'High Priority - Retain & Upsell'
        WHEN rfm_segment = 'Loyal Customers' THEN 'Medium Priority - Engage & Retain'
        WHEN rfm_segment = 'At Risk' THEN 'High Priority - Re-engage'
        WHEN rfm_segment = 'Can\'t Lose Them' THEN 'High Priority - Win Back'
        WHEN rfm_segment = 'About to Sleep' THEN 'Medium Priority - Re-engage'
        ELSE 'Low Priority - Win Back or Let Go'
    END as recommended_action
FROM rfm_segments
ORDER BY rfm_score DESC;

-- 4. CUSTOMER SEGMENTATION BY PROFITABILITY
SELECT 
    segment,
    region,
    COUNT(DISTINCT customer_id) as customer_count,
    SUM(total_sales) as segment_sales,
    SUM(total_profit) as segment_profit,
    AVG(total_sales) as avg_customer_sales,
    AVG(total_profit) as avg_customer_profit,
    (SUM(total_profit) / SUM(total_sales) * 100) as segment_profit_margin,
    AVG(total_orders) as avg_orders_per_customer
FROM (
    SELECT 
        customer_id,
        segment,
        region,
        COUNT(DISTINCT order_id) as total_orders,
        SUM(sales) as total_sales,
        SUM(profit) as total_profit
    FROM superstore
    GROUP BY customer_id, segment, region
) customer_summary
GROUP BY segment, region
ORDER BY segment_profit_margin DESC;

-- 5. CUSTOMER CHURN RISK ANALYSIS
WITH customer_activity AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        COUNT(DISTINCT order_id) as total_orders,
        SUM(sales) as total_sales,
        MAX(order_date) as last_order_date,
        DATEDIFF(CURRENT_DATE, MAX(order_date)) as days_since_last_order,
        AVG(DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date))) as avg_days_between_orders
    FROM superstore
    GROUP BY customer_id, customer_name, segment, region
),
churn_risk AS (
    SELECT 
        *,
        CASE 
            WHEN days_since_last_order <= 30 THEN 'Low Risk'
            WHEN days_since_last_order <= 60 THEN 'Medium Risk'
            WHEN days_since_last_order <= 90 THEN 'High Risk'
            ELSE 'Very High Risk'
        END as churn_risk_level,
        CASE 
            WHEN days_since_last_order > avg_days_between_orders * 2 THEN 'Likely Churned'
            WHEN days_since_last_order > avg_days_between_orders * 1.5 THEN 'At Risk'
            WHEN days_since_last_order > avg_days_between_orders THEN 'Watch'
            ELSE 'Active'
        END as churn_status
    FROM customer_activity
)
SELECT 
    *,
    CASE 
        WHEN churn_risk_level = 'Low Risk' THEN 'Continue current engagement'
        WHEN churn_risk_level = 'Medium Risk' THEN 'Increase engagement frequency'
        WHEN churn_risk_level = 'High Risk' THEN 'Re-engagement campaign'
        ELSE 'Win-back campaign'
    END as recommended_action
FROM churn_risk
ORDER BY days_since_last_order DESC;

-- 6. CUSTOMER VALUE GROWTH ANALYSIS
WITH customer_growth AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        YEAR(order_date) as order_year,
        COUNT(DISTINCT order_id) as orders_per_year,
        SUM(sales) as sales_per_year,
        SUM(profit) as profit_per_year
    FROM superstore
    GROUP BY customer_id, customer_name, segment, region, YEAR(order_date)
),
growth_metrics AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        MAX(CASE WHEN order_year = 2022 THEN sales_per_year ELSE 0 END) as sales_2022,
        MAX(CASE WHEN order_year = 2023 THEN sales_per_year ELSE 0 END) as sales_2023,
        MAX(CASE WHEN order_year = 2022 THEN profit_per_year ELSE 0 END) as profit_2022,
        MAX(CASE WHEN order_year = 2023 THEN profit_per_year ELSE 0 END) as profit_2023
    FROM customer_growth
    GROUP BY customer_id, customer_name, segment, region
)
SELECT 
    *,
    (sales_2023 - sales_2022) as sales_growth,
    (profit_2023 - profit_2022) as profit_growth,
    CASE 
        WHEN sales_2022 > 0 THEN ((sales_2023 - sales_2022) / sales_2022 * 100)
        ELSE NULL
    END as sales_growth_percentage,
    CASE 
        WHEN profit_2022 > 0 THEN ((profit_2023 - profit_2022) / profit_2022 * 100)
        ELSE NULL
    END as profit_growth_percentage,
    CASE 
        WHEN sales_2023 > sales_2022 THEN 'Growing'
        WHEN sales_2023 < sales_2022 THEN 'Declining'
        WHEN sales_2023 = sales_2022 THEN 'Stable'
        ELSE 'New Customer'
    END as growth_status
FROM growth_metrics
WHERE sales_2022 > 0 OR sales_2023 > 0
ORDER BY sales_growth_percentage DESC;

-- 7. CUSTOMER LIFETIME VALUE FORECASTING
WITH customer_metrics AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        COUNT(DISTINCT order_id) as total_orders,
        SUM(sales) as total_sales,
        SUM(profit) as total_profit,
        AVG(sales) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        DATEDIFF(MAX(order_date), MIN(order_date)) as customer_lifetime_days
    FROM superstore
    GROUP BY customer_id, customer_name, segment, region
),
clv_forecast AS (
    SELECT 
        *,
        -- Historical CLV
        total_profit as historical_clv,
        -- Predicted future orders (based on historical frequency)
        CASE 
            WHEN customer_lifetime_days > 0 THEN (365 / customer_lifetime_days) * total_orders
            ELSE total_orders
        END as predicted_annual_orders,
        -- Predicted future sales
        predicted_annual_orders * avg_order_value as predicted_annual_sales,
        -- Predicted future profit (assuming same margin)
        predicted_annual_sales * (total_profit / total_sales) as predicted_annual_profit,
        -- 3-year CLV forecast
        total_profit + (predicted_annual_profit * 3) as clv_3year_forecast,
        -- 5-year CLV forecast
        total_profit + (predicted_annual_profit * 5) as clv_5year_forecast
    FROM customer_metrics
    WHERE total_sales > 0
)
SELECT 
    *,
    CASE 
        WHEN clv_3year_forecast >= 10000 THEN 'Ultra High Value'
        WHEN clv_3year_forecast >= 5000 THEN 'High Value'
        WHEN clv_3year_forecast >= 2000 THEN 'Medium Value'
        WHEN clv_3year_forecast >= 1000 THEN 'Low Value'
        ELSE 'Minimal Value'
    END as forecasted_value_tier
FROM clv_forecast
ORDER BY clv_3year_forecast DESC;
