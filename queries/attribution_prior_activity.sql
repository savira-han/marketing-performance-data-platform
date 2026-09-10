-- == Prior Marketing Exposure among attributed bookings
-- grain : 1 row 1 campaign

WITH attributed_converters AS (
    SELECT
        customer_id,
        booking_id,
        booking_timestamp,
        attributed_campaign_id AS campaign_id
    FROM bookings
    WHERE attributed_campaign_id IS NOT NULL
),

attributed_campaign_touchpoint AS (
    SELECT
        a.customer_id,
        a.booking_id,
        a.booking_timestamp,
        a.campaign_id,
        t.timestamp AS attributed_touchpoint_timestamp
    FROM attributed_converters a
    JOIN touchpoints t
        ON a.customer_id = t.customer_id
        AND t.campaign_id = a.campaign_id
        AND t.timestamp < a.booking_timestamp
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY a.booking_id
        ORDER BY t.timestamp DESC
    ) = 1
),

prior_marketing AS (
    SELECT
        a.customer_id,
        a.booking_id,
        a.campaign_id,
        MAX(
            CASE
                WHEN t.timestamp < a.attributed_touchpoint_timestamp
                     AND t.campaign_id IS NOT NULL
                     AND t.campaign_id <> a.campaign_id
                THEN 1
                ELSE 0
            END
        ) AS had_prior_marketing
    FROM attributed_campaign_touchpoint a
    LEFT JOIN touchpoints t
        ON a.customer_id = t.customer_id
    GROUP BY
        a.customer_id,
        a.booking_id,
        a.campaign_id
)

SELECT
    campaign_id,
    COUNT(*) AS attributed_bookings,
    SUM(had_prior_marketing) AS bookings_with_prior_marketing,
    ROUND(
        100.0 * SUM(had_prior_marketing) / COUNT(*),
        2
    ) AS prior_marketing_rate
FROM prior_marketing
GROUP BY campaign_id
ORDER BY prior_marketing_rate DESC;