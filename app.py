"""
Marketing Performance Data Platform - Streamlit Dashboard

Purpose
-------
This application is the presentation layer of the analytics project.

The analytical logic remains in the SQL files under `queries/`.
This Streamlit app connects to the existing DuckDB database and
presents validated analytical results through an interactive dashboard.

Development workflow
--------------------
1. Data is generated and ingested into DuckDB.
2. Analytical SQL produces the business analysis.
3. Streamlit reads the analytical data from DuckDB.
4. The dashboard presents the results for stakeholder and recruiter review.
"""

from pathlib import Path

import duckdb
import streamlit as st


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="Marketing Performance Data Platform",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_ROOT / "analytics.duckdb"
QUERY_PATH = PROJECT_ROOT / "queries" / "customer_acquisition.sql"

CUSTOMER_QUALITY_QUERY_PATH = (
    PROJECT_ROOT / "queries" / "customer_quality.sql"
)

FUNNEL_GROWTH_QUERY_PATH = (
    PROJECT_ROOT / "queries" / "funnel_growth.sql"
)


# ============================================================
# Database connection
# ============================================================

con = duckdb.connect(
    str(DATABASE_PATH),
    read_only=True,
)


def load_sql(query_path):
    """Read an analytical SQL file from the queries directory."""
    return query_path.read_text()


# ============================================================
# Dashboard header
# ============================================================

st.title("Marketing Performance Data Platform")

st.write(
    "Interactive analysis of marketing acquisition efficiency, "
    "customer growth, and attribution integrity across 2025."
)

# ============================================================
# Marketing Performance
# ============================================================

st.header("Marketing Performance")


# ------------------------------------------------------------
# Executive KPIs
# ------------------------------------------------------------

st.subheader("Executive KPIs")

st.write(
    "Overall 2025 acquisition performance across all acquired "
    "customers and paid marketing activity."
)


# Total acquired customers
total_acquired_customers = con.execute("""
    SELECT COUNT(*) AS total_customers
    FROM customer_first_booking
""").fetchone()[0]


# Paid acquired customers
paid_acquired_customers = con.execute("""
    SELECT COUNT(*) AS paid_customers
    FROM customer_first_booking
    WHERE acquisition_source = 'Paid Campaign'
""").fetchone()[0]


# Paid acquisition share
paid_acquisition_share = (
    paid_acquired_customers
    / total_acquired_customers
    * 100
)


# Load campaign-level acquisition analysis
campaign_query = load_sql(QUERY_PATH)

campaign_df = con.execute(
    campaign_query
).fetchdf()


# ------------------------------------------------------------
# Normal campaign benchmark
# ------------------------------------------------------------
#
# CMP008 remains in the underlying analytical dataset because
# it is part of the attribution investigation.
#
# It is excluded from the primary campaign benchmark because
# its attribution pattern is anomalous.
# ------------------------------------------------------------

benchmark_df = campaign_df[
    campaign_df["campaign_id"] != "CMP008"
].copy()


# Aggregate economics for normal campaigns only
normal_campaign_spend = benchmark_df["total_spend"].sum()

normal_campaign_first_booking_value = (
    benchmark_df["total_first_booking_value"].sum()
)

normal_campaign_acquired_customers = (
    benchmark_df["acquired_customers"].sum()
)


normal_campaign_cac = (
    normal_campaign_spend
    / normal_campaign_acquired_customers
)

normal_campaign_roas = (
    normal_campaign_first_booking_value
    / normal_campaign_spend
)


# ------------------------------------------------------------
# KPI cards
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Acquired Customers",
        f"{total_acquired_customers:,}",
    )

with col2:
    st.metric(
        "Paid Acquisition Share",
        f"{paid_acquisition_share:.2f}%",
    )

with col3:
    st.metric(
        "Benchmark Campaign CAC",
        f"{normal_campaign_cac:,.2f}",
    )

with col4:
    st.metric(
        "Benchmark Campaign ROAS",
        f"{normal_campaign_roas:.2f}x",
    )


# ------------------------------------------------------------
# Campaign acquisition & economics
# ------------------------------------------------------------

st.subheader("Campaign Acquisition & Economics")

st.write(
    "Campaign-level acquisition performance based on 2025 spend, "
    "acquired customers, first-booking value, CAC, and ROAS. "
    "CMP008 is excluded from the primary benchmark and analyzed "
    "separately under Attribution Integrity."
)

# ------------------------------------------------------------
# Campaign benchmark table
# ------------------------------------------------------------

benchmark_display = benchmark_df[
    [
        "campaign_name",
        "acquired_customers",
        "total_spend",
        "avg_first_booking_value",
        "CAC",
        "ROAS",
    ]
].copy()


benchmark_display.columns = [
    "Campaign",
    "Acquired Customers",
    "Spend",
    "Avg First Booking",
    "CAC",
    "ROAS",
]


# Format values for dashboard display
benchmark_display["Acquired Customers"] = (
    benchmark_display["Acquired Customers"]
    .round(0)
    .astype(int)
)

benchmark_display["Spend"] = (
    benchmark_display["Spend"]
    .apply(lambda x: f"${x / 1000:,.0f}K")
)

benchmark_display["Avg First Booking"] = (
    benchmark_display["Avg First Booking"]
    .round(0)
    .apply(lambda x: f"${x:,.0f}")
)

benchmark_display["CAC"] = (
    benchmark_display["CAC"]
    .round(0)
    .apply(lambda x: f"${x:,.0f}")
)

benchmark_display["ROAS"] = (
    benchmark_display["ROAS"]
    .apply(lambda x: f"{x:.2f}x")
)


st.dataframe(
    benchmark_display,
    use_container_width=True,
    hide_index=True,
)



# ------------------------------------------------------------
# Campaign CAC ranking
# ------------------------------------------------------------

st.subheader("CAC by Campaign")

st.write(
    "Acquisition efficiency ranked by customer acquisition cost. "
    "Acquired customer volume is shown inside each bar."
)


# Prepare chart data
cac_chart_df = benchmark_df[
    [
        "campaign_name",
        "CAC",
        "acquired_customers",
    ]
].copy()

cac_chart_df = cac_chart_df.sort_values(
    "CAC",
    ascending=False,
)


# Create horizontal CAC bars
import altair as alt

bars = (
    alt.Chart(cac_chart_df)
    .mark_bar()
    .encode(
        x=alt.X(
            "CAC:Q",
            title="Customer Acquisition Cost",
            axis=alt.Axis(
                format="$,.0f",
            ),
        ),
        y=alt.Y(
            "campaign_name:N",
            title=None,
            sort=alt.EncodingSortField(
                field="CAC",
                order="ascending",
            ),
        ),
        tooltip=[
            alt.Tooltip(
                "campaign_name:N",
                title="Campaign",
            ),
            alt.Tooltip(
                "CAC:Q",
                title="CAC",
                format="$.0f",
            ),
            alt.Tooltip(
                "acquired_customers:Q",
                title="Acquired Customers",
                format=",",
            ),
        ],
    )
)


# Add acquired customer labels inside the bars
labels = (
    alt.Chart(cac_chart_df)
    .mark_text(
        align="right",
        baseline="middle",
        dx=-8,
        color="white"
    )
    .encode(
        x="CAC:Q",
        y=alt.Y(
            "campaign_name:N",
            sort=alt.EncodingSortField(
                field="CAC",
                order="ascending",
            ),
        ),
        text=alt.Text(
            "acquired_customers:Q",
            format=",",
        ),
    )
)


# Combine bars and labels
cac_chart = (
    (bars + labels)
    .properties(
        height=250,
    )
)


st.altair_chart(
    cac_chart,
    use_container_width=True,
)

# ------------------------------------------------------------
# Customer & Growth
# ------------------------------------------------------------

st.header("Customer & Growth")

# ------------------------------------------------------------
# Customer Quality
# ------------------------------------------------------------

st.subheader("Customer Quality")

st.write(
    "Acquired customers are segmented by observed booking frequency: "
    "One-time (1 booking), Repeat (2 bookings), and Frequent (3+ bookings)."
)


customer_quality_query = load_sql(
    CUSTOMER_QUALITY_QUERY_PATH
)

customer_quality_df = con.execute(
    customer_quality_query
).fetchdf()


# ------------------------------------------------------------
# Overall customer mix
# ------------------------------------------------------------

overall_quality = (
    customer_quality_df
    .groupby("customer_segment", as_index=False)
    .agg(
        acquired_customers=("acquired_customers", "sum")
    )
)

total_customers = overall_quality["acquired_customers"].sum()

overall_quality["share"] = (
    overall_quality["acquired_customers"]
    / total_customers
    * 100
)

segment_order = [
    "One-time",
    "Repeat",
    "Frequent",
]

overall_quality["sort_order"] = (
    overall_quality["customer_segment"]
    .map(
        {
            "One-time": 1,
            "Repeat": 2,
            "Frequent": 3,
        }
    )
)

overall_quality = (
    overall_quality
    .sort_values("sort_order")
)


# ------------------------------------------------------------
# Customer quality KPIs
# ------------------------------------------------------------

# col1, col2, col3 = st.columns(3)

# for col, segment in zip(
#     [col1, col2, col3],
#     segment_order,
# ):

#     row = overall_quality[
#         overall_quality["customer_segment"] == segment
#     ]

#     if not row.empty:

#         customers = int(
#             row["acquired_customers"].iloc[0]
#         )

#         share = row["share"].iloc[0]

#         with col:
#             st.metric(
#                 segment,
#                 f"{customers:,}",
#                 f"{share:.1f}% of acquired customers",
#             )

# ------------------------------------------------------------
# Customer quality KPIs
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }

    [data-testid="stMetricDelta"] {
        color: #1f77b4 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

for col, segment in zip(
    [col1, col2, col3],
    segment_order,
):

    row = overall_quality[
        overall_quality["customer_segment"] == segment
    ]

    if not row.empty:

        customers = int(
            row["acquired_customers"].iloc[0]
        )

        share = row["share"].iloc[0]

        with col:
            st.metric(
                segment,
                f"{customers:,}",
                f"{share:.1f}% of acquired customers",
                delta_color="off",
            )

# ------------------------------------------------------------
# Campaign customer quality comparison
# ------------------------------------------------------------

st.subheader("Customer Quality by Campaign")

st.write(
    "Customer mix and observed customer value across acquisition campaigns. "
    "Customer value reflects bookings observed during 2025."
)

campaign_quality = (
    customer_quality_df[
        [
            "campaign_name",
            "customer_segment",
            "acquired_customers",
            "avg_customer_value",
        ]
    ]
    .pivot(
        index="campaign_name",
        columns="customer_segment",
        values=[
            "acquired_customers",
            "avg_customer_value",
        ],
    )
    .reset_index()
)

campaign_quality.columns = [
    "_".join(col).strip("_")
    if isinstance(col, tuple)
    else col
    for col in campaign_quality.columns
]


# Calculate customer mix percentages
total_by_campaign = (
    campaign_quality[
        [
            "acquired_customers_One-time",
            "acquired_customers_Repeat",
            "acquired_customers_Frequent",
        ]
    ]
    .sum(axis=1)
)

campaign_quality["one_time_share"] = (
    campaign_quality["acquired_customers_One-time"]
    / total_by_campaign
    * 100
)

campaign_quality["repeat_share"] = (
    campaign_quality["acquired_customers_Repeat"]
    / total_by_campaign
    * 100
)

campaign_quality["frequent_share"] = (
    campaign_quality["acquired_customers_Frequent"]
    / total_by_campaign
    * 100
)


# Exclude CMP008 from the primary campaign comparison
campaign_quality = campaign_quality[
    campaign_quality["campaign_name"] != "Weekend Getaway"
].copy()


# Select dashboard columns
campaign_quality_display = campaign_quality[
    [
        "campaign_name",
        "one_time_share",
        "repeat_share",
        "frequent_share",
        "avg_customer_value_Repeat",
        "avg_customer_value_Frequent",
    ]
].copy()

campaign_quality_display.columns = [
    "Campaign",
    "One-time",
    "Repeat",
    "Frequent",
    "Repeat Customer Value",
    "Frequent Customer Value",
]


# Format values
campaign_quality_display["One-time"] = (
    campaign_quality_display["One-time"]
    .round(1)
    .apply(lambda x: f"{x:.1f}%")
)

campaign_quality_display["Repeat"] = (
    campaign_quality_display["Repeat"]
    .round(1)
    .apply(lambda x: f"{x:.1f}%")
)

campaign_quality_display["Frequent"] = (
    campaign_quality_display["Frequent"]
    .round(1)
    .apply(lambda x: f"{x:.1f}%")
)

campaign_quality_display["Repeat Customer Value"] = (
    campaign_quality_display["Repeat Customer Value"]
    .round(0)
    .apply(lambda x: f"${x:,.0f}")
)

campaign_quality_display["Frequent Customer Value"] = (
    campaign_quality_display["Frequent Customer Value"]
    .round(0)
    .apply(lambda x: f"${x:,.0f}")
)


st.dataframe(
    campaign_quality_display,
    use_container_width=True,
    hide_index=True,
)

# ------------------------------------------------------------
# Growth Over Time
# ------------------------------------------------------------

st.subheader("Booking Growth Over Time")

st.write(
    "Monthly booking volume split between new and repeat customers. "
    "This shows how existing customers increasingly contributed to "
    "booking volume over the year."
)

funnel_growth_query = load_sql(
    FUNNEL_GROWTH_QUERY_PATH
)

funnel_growth_df = con.execute(
    funnel_growth_query
).fetchdf()

# ------------------------------------------------------------
# Booking Growth Over Time
# ------------------------------------------------------------

st.subheader("Booking Growth Over Time")

st.write(
st.write(
    "Monthly booking volume split between new and repeat customers. "
    "Repeat bookings became a larger contributor to total booking volume "
    "as the year progressed."
)
)

funnel_growth_query = load_sql(
    FUNNEL_GROWTH_QUERY_PATH
)

funnel_growth_df = con.execute(
    funnel_growth_query
).fetchdf()


# Reshape booking types into columns
growth_chart_df = (
    funnel_growth_df
    .pivot(
        index="booking_month",
        columns="booking_type",
        values="bookings",
    )
    .reset_index()
)

growth_chart_df.columns.name = None

growth_chart_df["New"] = (
    growth_chart_df["New"]
    .fillna(0)
)

growth_chart_df["Repeat"] = (
    growth_chart_df["Repeat"]
    .fillna(0)
)

growth_chart_df["Total"] = (
    growth_chart_df["New"]
    + growth_chart_df["Repeat"]
)


# Format month for display
growth_chart_df["Month"] = (
    growth_chart_df["booking_month"]
    .dt.strftime("%Y-%m")
)

growth_chart_df = growth_chart_df.sort_values(
    "booking_month"
)


st.bar_chart(
    growth_chart_df.set_index("Month")[
        ["New", "Repeat"]
    ]
)

# ------------------------------------------------------------
# Attribution Integrity
# ------------------------------------------------------------

st.header("Attribution Integrity")

st.subheader("Attribution Methodology")

st.write(
    "Campaign attribution uses a last-touch model with a 30-day "
    "lookback window. Direct and Organic touchpoints are excluded "
    "from eligible marketing attribution."
)

st.info(
    "Attributed booking ≠ proven incremental booking. "
    "Attribution identifies which eligible marketing touchpoint "
    "receives reporting credit; it does not establish whether the "
    "booking would have happened without the campaign."
)

# ------------------------------------------------------------
# CMP008 Investigation
# ------------------------------------------------------------

st.subheader("CMP008 Attribution Anomaly")

st.write(
    "CMP008 was a short-lived campaign that showed an unusually "
    "high observed conversion rate and received attribution from "
    "customers who had already interacted with other marketing."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers Reached",
        "132",
    )

with col2:
    st.metric(
        "Customers Booked",
        "118",
    )

with col3:
    st.metric(
        "Attributed Bookings",
        "38",
    )

with col4:
    st.metric(
        "Prior Marketing Exposure",
        "94.7%",
    )

st.subheader("What the Anomaly Suggests")

st.write(
    "Of the 38 bookings attributed to CMP008, 36 customers (94.7%) "
    "had already been exposed to other marketing before interacting "
    "with CMP008. Combined with its unusually high observed conversion "
    "rate and short campaign duration, this makes the attribution "
    "pattern worth investigating."
)

st.warning(
    "CMP008 is excluded from primary campaign benchmarking. "
    "The observed pattern does not prove that CMP008 stole attribution "
    "or that its bookings were non-incremental. Establishing incremental "
    "impact would require a causal test such as a randomized holdout "
    "or geo-based experiment."
)

st.header("Business Recommendations")

st.write(
    "Recommendations are based on observed acquisition efficiency, "
    "customer value, and attribution reliability."
)

st.subheader("Campaign Recommendation")

recommendations = [
    (
        "Brand Search",
        "Continue and consider scaling. It combines the largest "
        "acquisition volume with the lowest CAC and highest ROAS "
        "among benchmarked campaigns."
    ),
    (
        "Hotel Deals",
        "Continue and consider additional investment. It shows "
        "similarly strong CAC and ROAS, with the highest average "
        "first-booking value among benchmarked campaigns."
    ),
    (
        "Generic Search",
        "Optimize before scaling. It provides meaningful acquisition "
        "volume but has higher CAC and lower ROAS than the leading campaigns."
    ),
    (
        "Summer Sale",
        "Review and optimize. Acquisition scale is meaningful, but "
        "efficiency is weaker than Brand Search and Hotel Deals."
    ),
    (
        "Travel Inspiration",
        "Validate before scaling. Acquisition efficiency is weaker, "
        "but frequent customers show relatively high observed value."
    ),
    (
        "CMP008",
        "Investigate separately. Its attribution pattern is unusual "
        "and should not be used as evidence for scaling decisions."
    ),
]

for campaign, recommendation in recommendations:
    st.markdown(f"**{campaign}** - {recommendation}")

# ============================================================
# Close database connection
# ============================================================

con.close()