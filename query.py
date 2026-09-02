import duckdb
import pandas as pd

# Connect to the DuckDB database
con = duckdb.connect("analytics.duckdb")

result = con.execute("""

-- ============================================================
-- Analytical Queries
-- ============================================================


-- ============================================================
-- 1. CAMPAIGN PERFORMANCE BY MONTH
-- ============================================================
-- Grain: one row per campaign × day.
--
-- This query rolls the daily data up to campaign × month.
-- Useful for analyzing seasonality and campaign trends over time.

SELECT
    campaign_id,
    DATE_TRUNC('month', date) AS month,

    SUM(total_spend) AS total_spend,
    SUM(total_impressions) AS total_impressions,
    SUM(total_clicks) AS total_clicks,
    SUM(total_bookings) AS total_bookings,
    SUM(attributed_revenue) AS attributed_revenue

FROM campaign_performance

WHERE date >= '2025-01-01'
  AND date < '2026-01-01'

GROUP BY
    campaign_id,
    month

ORDER BY
    campaign_id,
    month;


-- ============================================================
-- 2. CAMPAIGN FUNNEL — ANNUAL 2025
-- ============================================================
-- Aggregate its base metrics to campaign level
-- and calculate the funnel / efficiency metrics.


WITH campaign_totals AS (

    SELECT
        campaign_id,

        SUM(total_spend) AS total_spend,
        SUM(total_impressions) AS total_impressions,
        SUM(total_clicks) AS total_clicks,
        SUM(total_bookings) AS total_bookings,
        SUM(attributed_revenue) AS attributed_revenue

    FROM campaign_performance

    WHERE date >= '2025-01-01'
      AND date < '2026-01-01'

    GROUP BY
        campaign_id

)

SELECT
    campaign_id,

    -- Volume metrics
    total_spend,
    total_impressions,
    total_clicks,
    total_bookings,
    attributed_revenue,

    -- Funnel metrics
    total_clicks / total_impressions AS ctr,
    total_bookings / total_clicks AS conversion_rate,
    attributed_revenue / total_bookings AS avg_booking_value,

    -- Cost metrics
    total_spend / total_impressions * 1000 AS cpm,
    total_spend / total_clicks AS cpc,
    total_spend / total_bookings AS cpa,

    -- Revenue efficiency
    attributed_revenue / total_spend AS roas

FROM campaign_totals

ORDER BY
    total_spend DESC;


-- ============================================================
-- 3. CUSTOMER ACQUISITION BY CAMPAIGN
-- ============================================================
-- Acquisition definition:
--
-- A customer is acquired by the campaign receiving
-- last-click attribution for the customer's FIRST-EVER booking.
--
-- The first booking must be identified BEFORE filtering
-- to the 2025 analysis period.


WITH acquired_customer AS (

    SELECT
        campaign_id,
        customer_id,
        booking_timestamp,

        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY booking_timestamp ASC
        ) AS booking_rank

    FROM fact_booking_attribution

)

SELECT
    campaign_id,
    COUNT(DISTINCT customer_id) AS customer_acquired

FROM acquired_customer

WHERE booking_rank = 1
  AND booking_timestamp >= '2025-01-01'
  AND booking_timestamp < '2026-01-01'

GROUP BY
    campaign_id

ORDER BY
    customer_acquired DESC;


-- ============================================================
-- 4. CUSTOMER ACQUISITION VALUE
-- ============================================================
-- This extends the acquisition analysis above.
--
-- Use customer's first-ever booking to define
-- the acquisition campaign, then evaluate the value
-- of that first booking.
--
-- avg_booking_value is a BOOKING-level metric:
-- average revenue generated per booking.
--
-- Because the current dataset has one booking per customer,
-- it is numerically equal to revenue per acquired customer.
-- Conceptually, however, these are different metrics.


WITH acquired_customer AS (

    SELECT
        campaign_id,
        customer_id,
        booking_timestamp,
        booking_value,

        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY booking_timestamp ASC
        ) AS booking_rank

    FROM fact_booking_attribution

)

SELECT
    campaign_id,

    COUNT(DISTINCT customer_id) AS customer_acquired,

    SUM(booking_value) AS total_revenue_acquired,

    AVG(booking_value) AS avg_booking_value

FROM acquired_customer

WHERE booking_rank = 1
  AND booking_timestamp >= '2025-01-01'
  AND booking_timestamp < '2026-01-01'

GROUP BY
    campaign_id

ORDER BY
    customer_acquired DESC;


-- ============================================================
-- 5. DATA QUALITY CHECK — CAMPAIGN PERFORMANCE GRAIN
-- ============================================================
-- Validate that campaign_performance
-- actually has one row per campaign × day.
--
-- An empty result means there are no duplicate
-- campaign/date combinations.

SELECT
    campaign_id,
    date,
    COUNT(*) AS row_count

FROM campaign_performance

GROUP BY
    campaign_id,
    date

HAVING COUNT(*) > 1;

-- ============================================================
-- End of analytical query
-- ============================================================

""").fetchdf()

pd.set_option("display.max_columns",None)
print(result)

# ============================================================
# Close connection
# ============================================================

con.close()