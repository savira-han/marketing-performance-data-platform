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
-- Source model grain:
-- 1 row = 1 acquired customer
--
-- Final result grain:
-- 1 row = 1 campaign
-- ============================================================
WITH

campaign_performance as

(
    SELECT 
        campaign_id,
        SUM(spend) total_spend
    FROM ad_performance
    WHERE 
        date >= '2025-01-01'
        AND date < '2026-01-01'
    GROUP BY campaign_id
),

campaign_acquisition AS
(
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
)

SELECT
    cp.campaign_id, ca.campaign_name, ca.campaign_type, ca.channel_id, 
    cp.total_spend, ca.acquired_customers, ca.avg_first_booking_value, ca.total_first_booking_value, 
    ROUND(cp.total_spend/NULLIF(ca.acquired_customers,0),2) AS CAC, 
    ROUND(ca.total_first_booking_value/NULLIF(cp.total_spend,0),2) AS ROAS
FROM
    campaign_performance cp left join campaign_acquisition ca on cp.campaign_id = ca.acquisition_campaign_id
ORDER BY cp.total_spend DESC