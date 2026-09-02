import duckdb

# Connect to the DuckDB database
con = duckdb.connect("analytics.duckdb")


# ============================================================
# 1. BUILD FACT_BOOKING_ATTRIBUTION
# ============================================================
# Attribution method:
# - Last-click attribution
# - 30-day attribution window
# - Click-based touchpoints
#
# Grain:
# One booking with its attributed marketing touchpoint.
#
# This table connects each eligible booking to the
# marketing touchpoint that receives attribution.


DROP_FACT_BOOKING_ATTRIBUTION = """
DROP TABLE IF EXISTS fact_booking_attribution;
"""

con.execute(DROP_FACT_BOOKING_ATTRIBUTION)

con.execute("""

CREATE TABLE fact_booking_attribution AS

WITH booking_touchpoints AS (

    SELECT
        b.booking_id,
        b.customer_id,
        b.booking_timestamp,
        b.booking_value,

        t.touchpoint_id,
        t.timestamp AS touchpoint_timestamp,
        t.campaign_id,
        t.channel_id,

        ROW_NUMBER() OVER (
            PARTITION BY b.booking_id
            ORDER BY t.timestamp DESC
        ) AS touchpoint_rank

    FROM fact_booking AS b

    JOIN fact_marketing_touchpoint AS t
        ON b.customer_id = t.customer_id

    WHERE
        t.timestamp < b.booking_timestamp
        AND t.timestamp >= b.booking_timestamp - INTERVAL '30 days'

),

last_touch AS (

    SELECT
        booking_id,
        customer_id,
        booking_value,
        touchpoint_id,
        campaign_id,
        channel_id,
        touchpoint_timestamp,
        booking_timestamp

    FROM booking_touchpoints

    WHERE touchpoint_rank = 1

)

SELECT
    booking_id,
    customer_id,
    touchpoint_id,
    campaign_id,
    channel_id,
    touchpoint_timestamp,
    booking_timestamp,
    booking_value,
    'last_click' AS attribution_type,
    30 AS attribution_window_days,
    1 AS attributed_booking

FROM last_touch;

""")


# ============================================================
# 2. BUILD CAMPAIGN_PERFORMANCE
# ============================================================
# Grain:
# One campaign × one day.
#
# The table combines:
# - advertising performance
# - attributed bookings
# - attributed revenue
#
# Base metrics are stored instead of ratios such as CTR,
# CPC, CPA, and ROAS.
#
# This allows the table to be reused for different
# time periods and analytical dimensions.


con.execute("""

DROP TABLE IF EXISTS campaign_performance;

CREATE TABLE campaign_performance AS

WITH campaign_ad_performance AS (

    SELECT
        campaign_id,
        date,

        SUM(spend) AS total_spend,
        SUM(impressions) AS total_impressions,
        SUM(clicks) AS total_clicks

    FROM fact_ad_performance

    WHERE date >= '2025-01-01'
      AND date < '2026-01-01'

    GROUP BY
        campaign_id,
        date

),

campaign_booking_performance AS (

    SELECT
        campaign_id,
        CAST(booking_timestamp AS DATE) AS date,

        COUNT(booking_id) AS total_bookings,
        SUM(booking_value) AS attributed_revenue

    FROM fact_booking_attribution

    WHERE booking_timestamp >= '2025-01-01'
      AND booking_timestamp < '2026-01-01'

    GROUP BY
        campaign_id,
        CAST(booking_timestamp AS DATE)

)

SELECT
    a.campaign_id,
    a.date,

    a.total_spend,
    a.total_impressions,
    a.total_clicks,

    COALESCE(b.total_bookings, 0) AS total_bookings,
    COALESCE(b.attributed_revenue, 0) AS attributed_revenue

FROM campaign_ad_performance AS a

LEFT JOIN campaign_booking_performance AS b
    ON a.campaign_id = b.campaign_id
    AND a.date = b.date

ORDER BY
    a.campaign_id,
    a.date;

""")


# ============================================================
# CLOSE CONNECTION
# ============================================================

con.close()

print("Table build completed successfully.")