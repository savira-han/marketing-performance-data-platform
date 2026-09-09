-- ============================================================
-- Customer Quality Analysis
-- ============================================================
--
-- Business question:
-- What types of customers are acquired by each campaign?
-- How valuable are they?
-- How quickly do they come back?
--
-- Analytical lens:
-- 2025 customer acquisition cohort
--
-- Model used : acquired_customer_behavior
-- 
--
-- Final grain:
-- 1 row = 1 acquisition campaign × customer segment
-- ============================================================
WITH 

campaign_segment_agg AS

(
SELECT
    acquisition_campaign_id,
    customer_segment,

    COUNT(*) AS acquired_customers,

    -- composition
    -- COUNT(*) * 100.0
    --     / SUM(COUNT(*)) OVER (
    --         PARTITION BY acquisition_campaign_id
    --     ) AS customer_composition_pct,

    -- value
    AVG(total_booking_value) AS avg_customer_value,

    MEDIAN(total_booking_value) AS median_customer_value,

    -- rebooking
    AVG(days_to_second_booking)
        FILTER (
            WHERE days_to_second_booking IS NOT NULL
        ) AS avg_days_to_second_booking,

    MEDIAN(days_to_second_booking)
        FILTER (
            WHERE days_to_second_booking IS NOT NULL
        ) AS median_days_to_second_booking

FROM acquired_customer_behavior

GROUP BY
    acquisition_campaign_id,
    customer_segment
)

SELECT
    cs.acquisition_campaign_id,
    c.campaign_name,
    cs.customer_segment,
    cs.acquired_customers,
    cs.avg_customer_value,
    cs.median_customer_value,
    cs.avg_days_to_second_booking,
    cs.median_days_to_second_booking
FROM
 campaign_segment_agg cs LEFT JOIN campaigns c 
ON cs.acquisition_campaign_id = c.campaign_id