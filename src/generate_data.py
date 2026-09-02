import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# -------------------------
# 1. Generate channel data
# -------------------------

channels = [
    {
        "channel_id": "CH01",
        "channel_name": "Google Ads",
        "channel_group": "Paid Search"
    },
    {
        "channel_id": "CH02",
        "channel_name": "Meta",
        "channel_group": "Paid Social"
    },
    {
        "channel_id": "CH03",
        "channel_name": "TikTok",
        "channel_group": "Paid Social"
    }
]

df_channels = pd.DataFrame(channels)

df_channels.to_csv(
    "data/raw/channels.csv",
    index=False
)

print("Channel data generated successfully!")
print(df_channels)


# -------------------------
# 2. Generate campaign data
# -------------------------

campaigns = [
    {
        "campaign_id": "CMP001",
        "campaign_name": "Brand Search",
        "campaign_type": "Brand",
        "channel_id": "CH01"
    },
    {
        "campaign_id": "CMP002",
        "campaign_name": "Generic Search",
        "campaign_type": "Generic",
        "channel_id": "CH01"
    },
    {
        "campaign_id": "CMP003",
        "campaign_name": "Summer Sale",
        "campaign_type": "Promotion",
        "channel_id": "CH02"
    },
    {
        "campaign_id": "CMP004",
        "campaign_name": "Hotel Deals",
        "campaign_type": "Generic",
        "channel_id": "CH02"
    },
    {
        "campaign_id": "CMP005",
        "campaign_name": "Travel Inspiration",
        "campaign_type": "Awareness",
        "channel_id": "CH03"
    }
]

df_campaigns = pd.DataFrame(campaigns)

df_campaigns.to_csv(
    "data/raw/campaigns.csv",
    index=False
)


print("\nCampaign data generated successfully!")
print(df_campaigns)

# -------------------------
# 3. Generate customer data
# -------------------------

countries = [
    "Indonesia",
    "Thailand",
    "Singapore"
]

customers = []

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

days_between = (end_date - start_date).days

for i in range(1, 10001):

    random_days = random.randint(0, days_between)

    signup_date = start_date + timedelta(days=random_days)

    customer = {
        "customer_id": f"C{i:05d}",
        "country": random.choices(
            countries,
            weights=[0.60, 0.25, 0.15],
            k=1
        )[0],
        "signup_date": signup_date.strftime("%Y-%m-%d")
    }

    customers.append(customer)

df_customers = pd.DataFrame(customers)

# df_customers.to_csv(
#     "data/raw/customers.csv",
#     index=False
# )

print("\nCustomer data generated successfully!")
print(f"Number of customers: {len(df_customers)}")
print(df_customers.head())
print("\nCountry distribution:")
print(df_customers["country"].value_counts(normalize=True))

# -------------------------
# 4. Assign customer journey type
# -------------------------

journey_types = [
    "no_touchpoint",
    "non_converter",
    "converter"
]

customers_with_journey = []

for _, customer in df_customers.iterrows():

    journey_type = random.choices(
        journey_types,
        weights=[0.20, 0.45, 0.35],
        k=1
    )[0]

    customer_record = customer.to_dict()
    customer_record["journey_type"] = journey_type

    customers_with_journey.append(customer_record)

df_customers = pd.DataFrame(customers_with_journey)

df_customers.to_csv(
    "data/raw/customers.csv",
    index=False
)

print("\nCustomer journey types assigned!")
print(
    df_customers["journey_type"]
    .value_counts()
)

# -------------------------
# 5. Generate touchpoint data
# -------------------------

touchpoints = []

touchpoint_id = 1

campaign_weights = [0.25, 0.25, 0.20, 0.20, 0.10]

for _, customer in df_customers.iterrows():

    journey_type = customer["journey_type"]

    # Determine number of touchpoints
    if journey_type == "no_touchpoint":
        num_touchpoints = 0

    elif journey_type == "non_converter":
        num_touchpoints = random.choices(
            [1, 2, 3, 4],
            weights=[0.40, 0.35, 0.20, 0.05],
            k=1
        )[0]

    else:  # converter
        num_touchpoints = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.15, 0.30, 0.35, 0.15, 0.05],
            k=1
        )[0]

    # Generate the customer's journey
    if num_touchpoints > 0:

        journey_start = start_date + timedelta(
            days=random.randint(0, days_between)
        )

        current_timestamp = journey_start

        for _ in range(num_touchpoints):

            campaign = random.choices(
                campaigns,
                weights=campaign_weights,
                k=1
            )[0]

            touchpoint = {
                "touchpoint_id": f"T{touchpoint_id:06d}",
                "customer_id": customer["customer_id"],
                "timestamp": current_timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "channel_id": campaign["channel_id"],
                "campaign_id": campaign["campaign_id"]
            }

            touchpoints.append(touchpoint)

            touchpoint_id += 1

            # Move forward 1–7 days before next touchpoint
            current_timestamp += timedelta(
                days=random.randint(1, 7),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )


df_touchpoints = pd.DataFrame(touchpoints)

df_touchpoints.to_csv(
    "data/raw/touchpoints.csv",
    index=False
)

print("\nTouchpoint data generated successfully!")
print(f"Number of touchpoints: {len(df_touchpoints)}")
print(df_touchpoints.head())

# -------------------------
# 6. Generate booking data
# -------------------------

bookings = []

booking_id = 1

for _, customer in df_customers.iterrows():

    if customer["journey_type"] == "converter":

        # Get this customer's touchpoints
        customer_touchpoints = df_touchpoints[
            df_touchpoints["customer_id"] == customer["customer_id"]
        ]

        # Find the customer's last touchpoint
        last_touchpoint = customer_touchpoints.sort_values(
            "timestamp"
        ).iloc[-1]

        last_touchpoint_time = datetime.strptime(
            last_touchpoint["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        # Booking happens 1–3 days after last touchpoint
        booking_timestamp = last_touchpoint_time + timedelta(
            days=random.randint(1, 3),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        booking = {
            "booking_id": f"B{booking_id:06d}",
            "customer_id": customer["customer_id"],
            "booking_timestamp": booking_timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "booking_value": random.randint(100, 1500)
        }

        bookings.append(booking)

        booking_id += 1


df_bookings = pd.DataFrame(bookings)

df_bookings.to_csv(
    "data/raw/bookings.csv",
    index=False
)

print("\nBooking data generated successfully!")
print(f"Number of bookings: {len(df_bookings)}")
print(df_bookings.head())

# -------------------------
# 7. Generate ad performance data
# -------------------------

ad_performance = []

current_date = start_date

while current_date <= end_date:

    for campaign in campaigns:

        impressions = random.randint(5000, 50000)

        clicks = random.randint(
            int(impressions * 0.01),
            int(impressions * 0.08)
        )

        spend = round(
            random.uniform(100, 1000),
            2
        )

        ad_performance.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "campaign_id": campaign["campaign_id"],
            "spend": spend,
            "impressions": impressions,
            "clicks": clicks
        })

    current_date += timedelta(days=1)


df_ad_performance = pd.DataFrame(ad_performance)

df_ad_performance.to_csv(
    "data/raw/ad_performance.csv",
    index=False
)

print("\nAd performance data generated successfully!")
print(f"Number of ad performance rows: {len(df_ad_performance)}")
print(df_ad_performance.head())

# -------------------------
# Data quality checks
# -------------------------

print("\nRunning data quality checks...")

# Check 1: Customer IDs are unique
assert df_customers["customer_id"].is_unique

# Check 2: Touchpoint IDs are unique
assert df_touchpoints["touchpoint_id"].is_unique

# Check 3: Booking IDs are unique
assert df_bookings["booking_id"].is_unique

# Check 4: Every touchpoint customer exists
assert df_touchpoints["customer_id"].isin(
    df_customers["customer_id"]
).all()

# Check 5: Every booking customer exists
assert df_bookings["customer_id"].isin(
    df_customers["customer_id"]
).all()

# Check 6: Converter customers have bookings

converter_customers = df_customers[
    df_customers["journey_type"] == "converter"
]["customer_id"]

booking_customers = df_bookings["customer_id"]

assert set(converter_customers) == set(booking_customers)

# Check 7: Bookings happen after the final touchpoint

for _, booking in df_bookings.iterrows():

    customer_touchpoints = df_touchpoints[
        df_touchpoints["customer_id"] == booking["customer_id"]
    ]

    last_touchpoint_time = pd.to_datetime(
        customer_touchpoints["timestamp"]
    ).max()

    booking_time = pd.to_datetime(
        booking["booking_timestamp"]
    )

    assert booking_time > last_touchpoint_time

print("✓ Customer IDs are unique")
print("✓ Touchpoint IDs are unique")
print("✓ Booking IDs are unique")
print("✓ All touchpoint customers exist")
print("✓ All booking customers exist")
print("✓ Converter customers match booking customers")
print("✓ All bookings happen after the final touchpoint")

# -------------------------
# 8. Create fact_marketing_touchpoint
# -------------------------

df_touchpoints = pd.read_csv(
    "data/raw/touchpoints.csv"
)

fact_marketing_touchpoint = df_touchpoints[
    [
        "touchpoint_id",
        "customer_id",
        "timestamp",
        "campaign_id",
        "channel_id"
    ]
].copy()

fact_marketing_touchpoint["timestamp"] = pd.to_datetime(
    fact_marketing_touchpoint["timestamp"]
)

fact_marketing_touchpoint.to_csv(
    "data/processed/fact_marketing_touchpoint.csv",
    index=False
)

print("\nCreated fact_marketing_touchpoint!")
print(fact_marketing_touchpoint.head())

# -------------------------
# 9. Create dim_customer
# -------------------------

df_customers = pd.read_csv(
    "data/raw/customers.csv"
)

dim_customer = df_customers[
    [
        "customer_id",
        "country",
        "signup_date"
    ]
].copy()

dim_customer["signup_date"] = pd.to_datetime(
    dim_customer["signup_date"]
)

dim_customer.to_csv(
    "data/processed/dim_customer.csv",
    index=False
)

print("\nCreated dim_customer!")
print(dim_customer.head())

# -------------------------
# 10. Create dim_channel
# -------------------------

df_channels = pd.read_csv(
    "data/raw/channels.csv"
)

dim_channel = df_channels[
    [
        "channel_id",
        "channel_name"
    ]
].copy()

dim_channel.to_csv(
    "data/processed/dim_channel.csv",
    index=False
)

print("\nCreated dim_channel!")
print(dim_channel)

# -------------------------
# 11. Create dim_campaign
# -------------------------

df_campaigns = pd.read_csv(
    "data/raw/campaigns.csv"
)

dim_campaign = df_campaigns[
    [
        "campaign_id",
        "campaign_name",
        "channel_id"
    ]
].copy()

dim_campaign.to_csv(
    "data/processed/dim_campaign.csv",
    index=False
)

print("\nCreated dim_campaign!")
print(dim_campaign)

# -------------------------
# 12. Create fact_booking
# -------------------------

df_bookings = pd.read_csv(
    "data/raw/bookings.csv"
)

fact_booking = df_bookings[
    [
        "booking_id",
        "customer_id",
        "booking_timestamp",
        "booking_value"
    ]
].copy()

fact_booking["booking_timestamp"] = pd.to_datetime(
    fact_booking["booking_timestamp"]
)

fact_booking.to_csv(
    "data/processed/fact_booking.csv",
    index=False
)

print("\nCreated fact_booking!")
print(fact_booking.head())

# -------------------------
# 13. Create fact_ad_performance
# -------------------------

df_ad_performance = pd.read_csv(
    "data/raw/ad_performance.csv"
)

fact_ad_performance = df_ad_performance[
    [
        "date",
        "campaign_id",
        "spend",
        "impressions",
        "clicks"
    ]
].copy()

fact_ad_performance["date"] = pd.to_datetime(
    fact_ad_performance["date"]
)

fact_ad_performance.to_csv(
    "data/processed/fact_ad_performance.csv",
    index=False
)

print("\nCreated fact_ad_performance!")
print(fact_ad_performance.head())

# -------------------------
# 14. Create dim_date
# -------------------------

date_range = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

dim_date = pd.DataFrame({
    "date": date_range,
    "year": date_range.year,
    "month": date_range.month,
    "month_name": date_range.month_name(),
    "quarter": date_range.quarter,
    "day_of_week": date_range.day_name()
})

dim_date.to_csv(
    "data/processed/dim_date.csv",
    index=False
)

print("\nCreated dim_date!")
print(dim_date.head())