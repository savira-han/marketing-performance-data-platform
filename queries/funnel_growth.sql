-- == Customer Lens Conversion Rate by Campaign
-- == Grain : 1 row 1 campaign
SELECT
    t.campaign_id,
    COUNT(DISTINCT t.customer_id) AS customers_reached,
    COUNT(DISTINCT b.customer_id) AS customers_converted,
    ROUND(
        100.0 * COUNT(DISTINCT b.customer_id)
        / COUNT(DISTINCT t.customer_id),
        2
    ) AS customer_conversion_rate
FROM touchpoints t
LEFT JOIN bookings b
    ON t.customer_id = b.customer_id
    AND t.timestamp < b.booking_timestamp
GROUP BY t.campaign_id
ORDER BY customers_reached DESC;

-- == Repeat Booking Growth Monthly
WITH ranked_bookings AS (
    SELECT
        booking_id,
        customer_id,
        CAST(booking_timestamp AS TIMESTAMP) AS booking_timestamp,
        booking_value,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY CAST(booking_timestamp AS TIMESTAMP)
        ) AS booking_rank
    FROM bookings
)
SELECT
    DATE_TRUNC('month', booking_timestamp) AS booking_month,
    CASE
        WHEN booking_rank = 1 THEN 'New'
        ELSE 'Repeat'
    END AS booking_type,
    COUNT(*) AS bookings,
    ROUND(SUM(booking_value), 2) AS revenue
FROM ranked_bookings
WHERE
    booking_timestamp >= '2025-01-01'
    AND booking_timestamp < '2026-01-01'
GROUP BY
    booking_month,
    booking_type
ORDER BY
    booking_month,
    booking_type;