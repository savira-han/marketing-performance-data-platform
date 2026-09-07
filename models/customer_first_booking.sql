-- ============================================================
-- Customer First Booking Model
-- ============================================================
--
-- Grain:
-- 1 row = 1 customer with a first booking in 2025
--
-- Purpose:
-- Establish a reusable customer-level view of acquisition
-- and first-booking attributes.
--
-- Business rule:
-- A customer's acquisition campaign is the campaign attributed
-- to their first-ever booking.
--
-- Customers with no attributable non-direct campaign on their
-- first booking are classified as:
-- 'Organic / Direct / Unattributed'
-- ============================================================

WITH ranked_bookings AS (
    SELECT
        booking_id,
        customer_id,
        booking_timestamp,
        booking_value,
        attributed_campaign_id,

        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY CAST(booking_timestamp AS TIMESTAMP) ASC
        ) AS booking_rank

    FROM bookings
)

SELECT
    customer_id,
    booking_id AS first_booking_id,
    CAST(booking_timestamp AS TIMESTAMP) AS first_booking_timestamp,
    booking_value AS first_booking_value,
    attributed_campaign_id AS acquisition_campaign_id,

    CASE
        WHEN attributed_campaign_id IS NULL
            THEN 'Organic / Direct / Unattributed'
        ELSE 'Paid Campaign'
    END AS acquisition_source

FROM ranked_bookings

WHERE booking_rank = 1
  AND CAST(booking_timestamp AS TIMESTAMP) >= '2025-01-01'
  AND CAST(booking_timestamp AS TIMESTAMP) < '2026-01-01';