-- ============================================================
-- Customer Quality Analysis
-- ============================================================
--
-- Business question:
-- What does the booking behavior, rebooking speed, and
-- monetary value of each acquired customer look like?
--
-- Grain:
-- 1 row = 1 acquired customer
--
-- Analytical lens:
-- Customers whose first-ever booking was acquired in 2025
-- ============================================================

WITH 

ranked_bookings AS (

    SELECT
        customer_id,
        CAST(booking_timestamp AS TIMESTAMP) AS booking_timestamp,
        booking_value,

        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY CAST(booking_timestamp AS TIMESTAMP)
        ) AS booking_rank

    FROM bookings

),

customer_booking_behavior AS (

    SELECT
        customer_id,

        COUNT(*) AS total_bookings,

        ROUND(
            SUM(booking_value),
            2
        ) AS total_booking_value,

        ROUND(
            AVG(booking_value),
            2
        ) AS avg_booking_value,

        MIN(booking_timestamp)
            AS first_booking_timestamp,

        MIN(booking_timestamp)
            FILTER (WHERE booking_rank = 2)
            AS second_booking_timestamp

    FROM ranked_bookings

    GROUP BY customer_id

),

acquired_customer_behavior AS (

    SELECT
        fb.customer_id,
        fb.acquisition_campaign_id,
        fb.first_booking_timestamp,
        fb.first_booking_value,

        cb.total_bookings,
        cb.total_booking_value,
        cb.avg_booking_value,

        CASE
            WHEN cb.total_bookings = 1 THEN 'One-time'
            WHEN cb.total_bookings = 2 THEN 'Repeat'
            WHEN cb.total_bookings >= 3 THEN 'Frequent'
        END AS customer_segment,

        CASE
            WHEN cb.second_booking_timestamp IS NOT NULL
            THEN DATE_DIFF(
                'day',
                cb.first_booking_timestamp,
                cb.second_booking_timestamp
            )
            ELSE NULL
        END AS days_to_second_booking

    FROM customer_first_booking fb

    INNER JOIN customer_booking_behavior cb
        ON fb.customer_id = cb.customer_id

    WHERE fb.acquisition_source = 'Paid Campaign'

)

SELECT
    customer_id,
    acquisition_campaign_id,
    first_booking_timestamp,
    first_booking_value,
    total_bookings,
    total_booking_value,
    avg_booking_value,
    customer_segment,
    days_to_second_booking

FROM acquired_customer_behavior

ORDER BY customer_id;