-- ============================================================
-- Customer Acquisition Analysis
-- ============================================================
--
-- Business question:
-- How are customers acquired, and how does initial customer
-- value differ by acquisition source and campaign?
--
-- Source model:
-- customer_first_booking
--
-- Grain:
-- 1 row = 1 acquired customer
-- ============================================================

SELECT
    fb.acquisition_campaign_id,
    c.campaign_name,
    c.campaign_type,
    c.channel_id,

    COUNT(*) AS acquired_customers,

    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS acquisition_share_pct,

    ROUND(AVG(fb.first_booking_value), 2) AS avg_first_booking_value,

    ROUND(SUM(fb.first_booking_value), 2) AS total_first_booking_value

FROM customer_first_booking fb

LEFT JOIN campaigns c
    ON fb.acquisition_campaign_id = c.campaign_id

WHERE fb.acquisition_source = 'Paid Campaign'

GROUP BY
    fb.acquisition_campaign_id,
    c.campaign_name,
    c.campaign_type,
    c.channel_id

ORDER BY acquired_customers DESC;