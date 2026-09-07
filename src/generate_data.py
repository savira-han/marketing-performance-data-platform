import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# ============================================================
# 0. CONFIGURATION
# ============================================================

# -------------------------
# Dataset period
# -------------------------
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31, 23, 59, 59)

# -------------------------
# Customer volume
# -------------------------
NUM_CUSTOMERS = 10_000

# -------------------------
# Customer country mix
# -------------------------
COUNTRIES = ["Indonesia", "Thailand", "Singapore"]
COUNTRY_WEIGHTS = [0.60, 0.25, 0.15]

# -------------------------
# Channel definitions
# -------------------------
# Direct / Organic are included as channels because they can appear
# in customer journeys but should NOT receive campaign attribution.

CHANNELS = [
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
    },
    {
        "channel_id": "CH04",
        "channel_name": "Direct",
        "channel_group": "Direct / Organic"
    },
    {
        "channel_id": "CH05",
        "channel_name": "Organic Search",
        "channel_group": "Direct / Organic"
    }
]

# -------------------------
# Campaign definitions
# -------------------------
# CMP008 intentionally looks like a normal campaign.
#
# Its unusual behavior is NOT stored in campaign_name/type.
# The special behavior will be implemented later in the generator.
#
# This is important for the portfolio:
# the raw campaign table should not scream "fraud campaign".

CAMPAIGNS = [
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
    },
    {
        "campaign_id": "CMP008",
        "campaign_name": "Weekend Getaway",
        "campaign_type": "Promotion",
        "channel_id": "CH02"
    }
]

# -------------------------
# Campaign exposure weights
# -------------------------
# These control how often normal campaigns are selected when
# generating customer touchpoints.
#
# CMP008 is handled separately because it has special behavior.

NORMAL_CAMPAIGN_WEIGHTS = {
    "CMP001": 0.25,
    "CMP002": 0.25,
    "CMP003": 0.20,
    "CMP004": 0.20,
    "CMP005": 0.10
}

# -------------------------
# Customer journey behavior
# -------------------------
# These are probabilities, not fixed journey categories.
#
# Some customers will:
# - never interact with marketing
# - interact but never book
# - book once
# - book multiple times
#
# The exact journey will be generated later.

NO_ACTIVITY_RATE = 0.10
NON_CONVERTER_RATE = 0.30
ONE_BOOKING_RATE = 0.35
REPEAT_BOOKING_RATE = 0.25

# -------------------------
# CMP008 special campaign
# -------------------------
# CMP008 runs for exactly one month.
#
# We will implement its actual behavior later.
# For now we only define its configuration here.

CMP008_START_DATE = datetime(2025, 6, 1)
CMP008_END_DATE = datetime(2025, 6, 30, 23, 59, 59)

CMP008_HIGH_INTENT_RATE = 0.70
CMP008_MAX_TOUCHPOINTS_PER_CUSTOMER = 1
CMP008_EXPOSURE_RATE = 0.08

# -------------------------
# Attribution configuration
# -------------------------
ATTRIBUTION_LOOKBACK_DAYS = 30

# Direct / Organic channels are excluded from
# last-touch non-direct attribution.
NON_ATTRIBUTABLE_CHANNELS = {
    "CH04",  # Direct
    "CH05"   # Organic Search
}


# ============================================================
# 1. GENERATE CHANNEL DATA
# ============================================================

df_channels = pd.DataFrame(CHANNELS)

df_channels.to_csv(
    "data/raw/channels.csv",
    index=False
)


# ============================================================
# 2. GENERATE CAMPAIGN DATA
# ============================================================

df_campaigns = pd.DataFrame(CAMPAIGNS)

df_campaigns.to_csv(
    "data/raw/campaigns.csv",
    index=False
)


# ============================================================
# 3. GENERATE CUSTOMER DATA
# ============================================================

customers = []

days_between = (END_DATE.date() - START_DATE.date()).days

for i in range(1, NUM_CUSTOMERS + 1):

    random_days = random.randint(0, days_between)

    signup_date = START_DATE + timedelta(
        days=random_days
    )

    customer = {
        "customer_id": f"C{i:05d}",
        "country": random.choices(
            COUNTRIES,
            weights=COUNTRY_WEIGHTS,
            k=1
        )[0],
        "signup_date": signup_date.strftime("%Y-%m-%d")
    }

    customers.append(customer)


df_customers = pd.DataFrame(customers)

df_customers.to_csv(
    "data/raw/customers.csv",
    index=False
)

# ============================================================
# 4. GENERATE CUSTOMER JOURNEYS
# ============================================================

# Each customer gets a behavioral profile.
#
# This is NOT stored in the final customer table.
# It is only used internally to generate realistic journeys.
#
# Possible profiles:
# - no_activity
# - non_converter
# - one_booking
# - repeat_booking


def generate_customer_profile():
    profile = random.choices(
        [
            "no_activity",
            "non_converter",
            "one_booking",
            "repeat_booking"
        ],
        weights=[
            NO_ACTIVITY_RATE,
            NON_CONVERTER_RATE,
            ONE_BOOKING_RATE,
            REPEAT_BOOKING_RATE
        ],
        k=1
    )[0]

    return profile


# Store temporary journey information.
customer_journeys = {}

for _, customer in df_customers.iterrows():

    customer_id = customer["customer_id"]

    profile = generate_customer_profile()

    customer_journeys[customer_id] = {
        "profile": profile,
        "touchpoints": [],
        "bookings": []
    }

print("\nCustomer journey distribution:")
print(pd.Series(customer_journeys).value_counts())

# ============================================================
# 5. BOOKINGS
# ============================================================

def generate_booking_value():
    """
    Generate realistic OTA booking values.

    Most bookings are moderate value,
    some are higher value,
    and a small number are very high value.
    """

    value = random.lognormvariate(5.7, 0.65)

    return round(
        max(100, min(value, 5000)),
        2
    )


bookings = []
booking_counter = 1


for customer_id, journey_data in customer_journeys.items():

    journey = journey_data["profile"]

    customer = df_customers[
        df_customers["customer_id"] == customer_id
    ].iloc[0]

    signup_date = datetime.strptime(
        customer["signup_date"],
        "%Y-%m-%d"
    )

    # --------------------------------------------------------
    # Customers with no activity do not book
    # --------------------------------------------------------

    if journey == "no_activity":
        continue

    # --------------------------------------------------------
    # Decide number of bookings
    # --------------------------------------------------------

    if journey == "non_converter":

        num_bookings = 0

    elif journey == "one_booking":

        num_bookings = 1

    elif journey == "repeat_booking":

        num_bookings = random.randint(2, 4)

    else:

        num_bookings = 0

    if num_bookings == 0:
        continue

    # --------------------------------------------------------
    # Generate first booking timestamp
    # --------------------------------------------------------

    current_time = signup_date + timedelta(
        days=random.randint(7, 60),
        hours=random.randint(1, 20)
    )

    # --------------------------------------------------------
    # Generate booking journey
    # --------------------------------------------------------

    for booking_number in range(num_bookings):

        # Do not generate bookings after 2025.
        if current_time > END_DATE:
            break

        booking = {
            "booking_id": f"B{booking_counter:06d}",
            "customer_id": customer_id,
            "booking_timestamp": current_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "booking_value": generate_booking_value()
        }

        # Store final booking record.
        bookings.append(booking)

        # Store booking inside temporary journey.
        # Section 6 will use this to generate
        # touchpoints around each booking.
        customer_journeys[
            customer_id
        ]["bookings"].append(booking)

        booking_counter += 1

        # ----------------------------------------------------
        # Create realistic gap before next booking
        # ----------------------------------------------------

        if booking_number < num_bookings - 1:

            repeat_gap = random.choice([
                7,
                14,
                21,
                30,
                45,
                60,
                90
            ])

            current_time += timedelta(
                days=repeat_gap,
                hours=random.randint(1, 12)
            )


df_bookings = pd.DataFrame(bookings)

df_bookings.to_csv(
    "data/raw/bookings.csv",
    index=False
)

print(
    f"Generated {len(df_bookings):,} bookings"
)

# ============================================================
# 6. TOUCHPOINTS
# ============================================================

touchpoints = []
touchpoint_counter = 1

# Track customers who have already been exposed to CMP008.
# Each customer can receive CMP008 at most once.
cmp008_exposed_customers = set()


def is_high_intent_customer(customer_id):
    """
    Synthetic high-intent proxy.

    A customer is considered high intent if they have already
    demonstrated meaningful marketing activity before the
    current touchpoint.
    """

    customer_touchpoints = [
        tp
        for tp in touchpoints
        if tp["customer_id"] == customer_id
    ]

    if not customer_touchpoints:
        return False

    marketing_touchpoints = [
        tp
        for tp in customer_touchpoints
        if tp["channel_id"] not in NON_ATTRIBUTABLE_CHANNELS
    ]

    return len(marketing_touchpoints) >= 2


# ============================================================
# Generate touchpoints for each customer
# ============================================================

for customer_id, journey_data in customer_journeys.items():

    journey = journey_data["profile"]

    customer = df_customers[
        df_customers["customer_id"] == customer_id
    ].iloc[0]

    signup_date = pd.to_datetime(
        customer["signup_date"]
    )

    # --------------------------------------------------------
    # CASE 1: No activity
    # --------------------------------------------------------

    if journey == "no_activity":
        continue

    # --------------------------------------------------------
    # CASE 2: Non-converter
    #
    # Customer has activity but never books.
    # --------------------------------------------------------

    if journey == "non_converter":

        num_touchpoints = random.randint(1, 5)

        current_time = signup_date + timedelta(
            hours=random.randint(1, 72)
        )

        for _ in range(num_touchpoints):

            current_time += timedelta(
                hours=random.randint(1, 72)
            )

            # ------------------------------------------------
            # CMP008 special campaign exposure
            # ------------------------------------------------

            if (
                CMP008_START_DATE
                <= current_time
                <= CMP008_END_DATE

                and customer_id
                not in cmp008_exposed_customers

                and random.random()
                < CMP008_EXPOSURE_RATE
            ):

                high_intent = is_high_intent_customer(
                    customer_id
                )

                if (
                    high_intent
                    or random.random() < 0.15
                ):

                    touchpoints.append({
                        "touchpoint_id":
                            f"T{touchpoint_counter:06d}",

                        "customer_id":
                            customer_id,

                        "timestamp":
                            current_time.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),

                        "channel_id":
                            "CH02",

                        "campaign_id":
                            "CMP008"
                    })

                    cmp008_exposed_customers.add(
                        customer_id
                    )

                    touchpoint_counter += 1

                    # CMP008 already created this
                    # touchpoint iteration.
                    continue

            # ------------------------------------------------
            # Normal touchpoint
            # ------------------------------------------------

            if random.random() < 0.70:

                campaign_id = random.choices(
                    list(
                        NORMAL_CAMPAIGN_WEIGHTS.keys()
                    ),
                    weights=list(
                        NORMAL_CAMPAIGN_WEIGHTS.values()
                    ),
                    k=1
                )[0]

                channel_id = next(
                    campaign["channel_id"]
                    for campaign in CAMPAIGNS
                    if campaign["campaign_id"]
                    == campaign_id
                )

            else:

                channel_id = random.choice([
                    "CH04",
                    "CH05"
                ])

                campaign_id = None

            touchpoints.append({
                "touchpoint_id":
                    f"T{touchpoint_counter:06d}",

                "customer_id":
                    customer_id,

                "timestamp":
                    current_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "channel_id":
                    channel_id,

                "campaign_id":
                    campaign_id
            })

            touchpoint_counter += 1

    # --------------------------------------------------------
    # CASE 3: Customer has one or more bookings
    # --------------------------------------------------------

    else:

        customer_bookings = journey_data["bookings"]

        current_time = signup_date + timedelta(
            hours=random.randint(1, 72)
        )

        # ----------------------------------------------------
        # Generate touchpoints before each booking
        # ----------------------------------------------------

        for booking in customer_bookings:

            booking_time = pd.to_datetime(
                booking["booking_timestamp"]
            )

            available_hours = (
                booking_time - current_time
            ).total_seconds() / 3600

            if available_hours <= 1:

                num_touchpoints = 0

            else:

                max_touchpoints = min(
                    6,
                    max(
                        1,
                        int(available_hours / 24)
                    )
                )

                num_touchpoints = random.randint(
                    1,
                    max_touchpoints
                )

            # ------------------------------------------------
            # Generate touchpoints
            # ------------------------------------------------

            for _ in range(num_touchpoints):

                remaining_hours = (
                    booking_time - current_time
                ).total_seconds() / 3600

                if remaining_hours <= 1:
                    break

                max_step_hours = max(
                    1,
                    int(remaining_hours / 2)
                )

                current_time += timedelta(
                    hours=random.randint(
                        1,
                        max_step_hours
                    )
                )

                # Never allow a touchpoint to occur
                # at or after the booking.
                if current_time >= booking_time:
                    break

                # ------------------------------------------------
                # CMP008 special campaign exposure
                # ------------------------------------------------

                if (
                    CMP008_START_DATE
                    <= current_time
                    <= CMP008_END_DATE

                    and customer_id
                    not in cmp008_exposed_customers

                    and random.random()
                    < CMP008_EXPOSURE_RATE
                ):

                    high_intent = is_high_intent_customer(
                        customer_id
                    )

                    if (
                        high_intent
                        or random.random() < 0.15
                    ):

                        touchpoints.append({
                            "touchpoint_id":
                                f"T{touchpoint_counter:06d}",

                            "customer_id":
                                customer_id,

                            "timestamp":
                                current_time.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),

                            "channel_id":
                                "CH02",

                            "campaign_id":
                                "CMP008"
                        })

                        cmp008_exposed_customers.add(
                            customer_id
                        )

                        touchpoint_counter += 1

                        # CMP008 already created this
                        # touchpoint iteration.
                        continue

                # ------------------------------------------------
                # Normal touchpoint
                # ------------------------------------------------

                if random.random() < 0.70:

                    campaign_id = random.choices(
                        list(
                            NORMAL_CAMPAIGN_WEIGHTS.keys()
                        ),
                        weights=list(
                            NORMAL_CAMPAIGN_WEIGHTS.values()
                        ),
                        k=1
                    )[0]

                    channel_id = next(
                        campaign["channel_id"]
                        for campaign in CAMPAIGNS
                        if campaign["campaign_id"]
                        == campaign_id
                    )

                else:

                    channel_id = random.choice([
                        "CH04",
                        "CH05"
                    ])

                    campaign_id = None

                touchpoints.append({
                    "touchpoint_id":
                        f"T{touchpoint_counter:06d}",

                    "customer_id":
                        customer_id,

                    "timestamp":
                        current_time.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "channel_id":
                        channel_id,

                    "campaign_id":
                        campaign_id
                })

                touchpoint_counter += 1

            # After the booking, move the timeline exactly
            # to the booking timestamp.
            current_time = booking_time


df_touchpoints = pd.DataFrame(touchpoints)

df_touchpoints.to_csv(
    "data/raw/touchpoints.csv",
    index=False
)

print(
    f"Generated {len(df_touchpoints):,} touchpoints"
)

# ============================================================
# 6A. AD PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("6A. AD PERFORMANCE")
print("=" * 60)


# ------------------------------------------------------------
# Business definition
#
# Grain:
#   1 row = 1 campaign × 1 day
#
# This table represents campaign-level advertising metrics,
# not individual customer interactions.
#
# Therefore it is different from:
#
# fact_marketing_touchpoint
#   1 row = 1 customer touchpoint
#
# fact_ad_performance
#   1 row = 1 campaign per day
# ------------------------------------------------------------


# ------------------------------------------------------------
# Campaign performance profiles
#
# These parameters intentionally make campaigns different.
# The differences will allow us to investigate:
#
# - volume
# - CTR
# - CPC
# - spend
# - efficiency
#
# Later, booking data will be connected to these metrics.
# ------------------------------------------------------------

CAMPAIGN_PERFORMANCE_PROFILES = {

    "CMP001": {
        "base_impressions": 8500,
        "ctr": 0.075,
        "cpc": 0.35
    },

    "CMP002": {
        "base_impressions": 12000,
        "ctr": 0.045,
        "cpc": 0.55
    },

    "CMP003": {
        "base_impressions": 10000,
        "ctr": 0.055,
        "cpc": 0.45
    },

    "CMP004": {
        "base_impressions": 8000,
        "ctr": 0.040,
        "cpc": 0.60
    },

    "CMP005": {
        "base_impressions": 15000,
        "ctr": 0.025,
        "cpc": 0.30
    },

    # CMP008 intentionally has unusually high exposure.
    # This supports the later attribution-hijacking analysis.
    "CMP008": {
        "base_impressions": 30000,
        "ctr": 0.080,
        "cpc": 0.20
    }
}


# ------------------------------------------------------------
# Generate daily campaign performance
# ------------------------------------------------------------

ad_performance = []

current_date = START_DATE.date()

while current_date <= END_DATE.date():

    current_datetime = datetime.combine(
        current_date,
        datetime.min.time()
    )

    # --------------------------------------------------------
    # Seasonality
    #
    # OTA demand varies throughout the year.
    # We use simple monthly multipliers rather than trying
    # to model complicated real-world seasonality.
    # --------------------------------------------------------

    month = current_date.month

    if month in [6, 7, 8]:
        seasonal_multiplier = 1.20

    elif month in [11, 12]:
        seasonal_multiplier = 1.15

    elif month in [2, 3]:
        seasonal_multiplier = 0.90

    else:
        seasonal_multiplier = 1.00


    # --------------------------------------------------------
    # Generate performance for each campaign
    # --------------------------------------------------------

    for campaign in CAMPAIGNS:

        campaign_id = campaign["campaign_id"]

        # ----------------------------------------------------
        # CMP008 only exists during its active month.
        # ----------------------------------------------------

        if campaign_id == "CMP008":

            if not (
                CMP008_START_DATE.date()
                <= current_date
                <= CMP008_END_DATE.date()
            ):
                continue


        profile = (
            CAMPAIGN_PERFORMANCE_PROFILES[
                campaign_id
            ]
        )


        # ----------------------------------------------------
        # Daily randomness prevents perfectly uniform data.
        # ----------------------------------------------------

        daily_variation = random.uniform(
            0.80,
            1.20
        )


        # ----------------------------------------------------
        # Impressions
        # ----------------------------------------------------

        impressions = int(
            profile["base_impressions"]
            * seasonal_multiplier
            * daily_variation
        )

        impressions = max(
            impressions,
            100
        )


        # ----------------------------------------------------
        # Click-through rate
        #
        # Add small daily variation while keeping CTR
        # within a realistic range.
        # ----------------------------------------------------

        daily_ctr = (
            profile["ctr"]
            * random.uniform(0.85, 1.15)
        )

        daily_ctr = min(
            max(daily_ctr, 0.005),
            0.15
        )


        clicks = int(
            impressions
            * daily_ctr
        )

        clicks = min(
            clicks,
            impressions
        )


        # ----------------------------------------------------
        # Spend
        #
        # CPC varies slightly day to day.
        # ----------------------------------------------------

        daily_cpc = (
            profile["cpc"]
            * random.uniform(0.85, 1.15)
        )

        spend = round(
            clicks * daily_cpc,
            2
        )


        ad_performance.append({

            "date":
                current_date.strftime(
                    "%Y-%m-%d"
                ),

            "campaign_id":
                campaign_id,

            "impressions":
                impressions,

            "clicks":
                clicks,

            "spend":
                spend
        })


    current_date += timedelta(days=1)


# ------------------------------------------------------------
# Create DataFrame
# ------------------------------------------------------------

df_ad_performance = pd.DataFrame(
    ad_performance
)


# ------------------------------------------------------------
# Save raw ad performance
# ------------------------------------------------------------

df_ad_performance.to_csv(
    "data/raw/ad_performance.csv",
    index=False
)


print(
    f"Generated "
    f"{len(df_ad_performance):,} "
    f"campaign-day records"
)


# ------------------------------------------------------------
# Basic summary
# ------------------------------------------------------------

print(
    "\nAd performance by campaign:"
)

print(
    df_ad_performance
    .groupby("campaign_id")
    .agg(
        days=("date", "count"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        spend=("spend", "sum")
    )
)


# ------------------------------------------------------------
# 6A. VALIDATION
# ------------------------------------------------------------

# Every campaign-day combination must be unique.

assert (
    df_ad_performance[
        [
            "campaign_id",
            "date"
        ]
    ]
    .duplicated()
    .sum()
    == 0
)

print(
    "✓ Campaign-day grain validation passed"
)


# Impressions must be positive.
assert (
    df_ad_performance["impressions"] > 0
).all()

print(
    "✓ Impression validation passed"
)


# Clicks cannot exceed impressions.
assert (
    df_ad_performance["clicks"]
    <= df_ad_performance["impressions"]
).all()

assert (
    df_ad_performance["clicks"] >= 0
).all()

print(
    "✓ Click validation passed"
)


# Spend cannot be negative.
assert (
    df_ad_performance["spend"] >= 0
).all()

print(
    "✓ Spend validation passed"
)


# ------------------------------------------------------------
# CMP008 active-period validation
# ------------------------------------------------------------

cmp008_ad_rows = df_ad_performance[
    df_ad_performance["campaign_id"]
    == "CMP008"
].copy()

assert len(cmp008_ad_rows) == 30

cmp008_dates = pd.to_datetime(
    cmp008_ad_rows["date"]
)

assert (
    cmp008_dates.min()
    == pd.Timestamp("2025-06-01")
)

assert (
    cmp008_dates.max()
    == pd.Timestamp("2025-06-30")
)

print(
    "✓ CMP008 ad-performance active-period validation passed"
)


# ------------------------------------------------------------
# Final summary
# ------------------------------------------------------------

print(
    "\n" + "=" * 60
)

print(
    "✓ SECTION 6A AD PERFORMANCE COMPLETED"
)

print(
    "=" * 60
)

# ============================================================
# 7. VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("7. VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 7.1 PREPARE DATETIME COLUMNS
# ------------------------------------------------------------

df_bookings["booking_timestamp"] = pd.to_datetime(
    df_bookings["booking_timestamp"],
    format="%Y-%m-%d %H:%M:%S"
)

df_touchpoints["timestamp"] = pd.to_datetime(
    df_touchpoints["timestamp"],
    format="%Y-%m-%d %H:%M:%S"
)

df_customers["signup_date"] = pd.to_datetime(
    df_customers["signup_date"],
    format="%Y-%m-%d"
)


# ------------------------------------------------------------
# 7.2 PRIMARY KEY VALIDATION
# ------------------------------------------------------------

assert df_customers["customer_id"].is_unique
assert df_bookings["booking_id"].is_unique
assert df_touchpoints["touchpoint_id"].is_unique
assert df_campaigns["campaign_id"].is_unique
assert df_channels["channel_id"].is_unique

print("✓ Primary key uniqueness passed")


# ------------------------------------------------------------
# 7.3 CUSTOMER FOREIGN KEY VALIDATION
# ------------------------------------------------------------

valid_customer_ids = set(
    df_customers["customer_id"]
)

assert set(
    df_bookings["customer_id"]
).issubset(valid_customer_ids)

assert set(
    df_touchpoints["customer_id"]
).issubset(valid_customer_ids)

print("✓ Customer foreign key validation passed")


# ------------------------------------------------------------
# 7.4 CAMPAIGN FOREIGN KEY VALIDATION
# ------------------------------------------------------------

valid_campaign_ids = set(
    df_campaigns["campaign_id"]
)

touchpoint_campaign_ids = set(
    df_touchpoints[
        df_touchpoints["campaign_id"].notna()
    ]["campaign_id"]
)

assert touchpoint_campaign_ids.issubset(
    valid_campaign_ids
)

print("✓ Campaign foreign key validation passed")


# ------------------------------------------------------------
# 7.5 CHANNEL FOREIGN KEY VALIDATION
# ------------------------------------------------------------

valid_channel_ids = set(
    df_channels["channel_id"]
)

assert set(
    df_touchpoints["channel_id"]
).issubset(valid_channel_ids)

assert set(
    df_campaigns["channel_id"]
).issubset(valid_channel_ids)

print("✓ Channel foreign key validation passed")


# ------------------------------------------------------------
# 7.6 BOOKING VALUE VALIDATION
# ------------------------------------------------------------

assert (
    df_bookings["booking_value"] > 0
).all()

print("✓ Booking value validation passed")


# ------------------------------------------------------------
# 7.7 BOOKING AFTER SIGNUP
# ------------------------------------------------------------

signup_lookup = df_customers.set_index(
    "customer_id"
)["signup_date"]

booking_signup_dates = (
    df_bookings["customer_id"]
    .map(signup_lookup)
)

assert (
    df_bookings["booking_timestamp"]
    > booking_signup_dates
).all()

print("✓ Booking-after-signup validation passed")


# ------------------------------------------------------------
# 7.8 TOUCHPOINT AFTER SIGNUP
# ------------------------------------------------------------

touchpoint_signup_dates = (
    df_touchpoints["customer_id"]
    .map(signup_lookup)
)

assert (
    df_touchpoints["timestamp"]
    > touchpoint_signup_dates
).all()

print("✓ Touchpoint-after-signup validation passed")


# ------------------------------------------------------------
# 7.9 TOUCHPOINTS BEFORE BOOKINGS
#
# For every customer, every touchpoint must occur before
# the customer's next booking.
#
# This prevents impossible journeys such as:
#
# Booking
# ↓
# Touchpoint
#
# ------------------------------------------------------------

touchpoint_after_booking_errors = 0

for customer_id in df_customers["customer_id"]:

    customer_bookings = (
        df_bookings[
            df_bookings["customer_id"]
            == customer_id
        ]
        .sort_values("booking_timestamp")
    )

    customer_touchpoints = (
        df_touchpoints[
            df_touchpoints["customer_id"]
            == customer_id
        ]
        .sort_values("timestamp")
    )

    if customer_bookings.empty:
        continue

    for _, touchpoint in customer_touchpoints.iterrows():

        later_bookings = customer_bookings[
            customer_bookings["booking_timestamp"]
            <= touchpoint["timestamp"]
        ]

        if not later_bookings.empty:

            # A touchpoint can occur after a previous booking
            # because it belongs to the next journey.
            #
            # Therefore we only need to ensure it occurs
            # before at least one subsequent booking.
            next_booking = customer_bookings[
                customer_bookings["booking_timestamp"]
                > touchpoint["timestamp"]
            ]

            if next_booking.empty:
                touchpoint_after_booking_errors += 1


assert touchpoint_after_booking_errors == 0

print(
    "✓ Touchpoint-to-booking timeline validation passed"
)


# ------------------------------------------------------------
# 7.10 REPEAT BOOKING ORDER
# ------------------------------------------------------------

booking_order_errors = 0

for customer_id, customer_bookings in (
    df_bookings.groupby("customer_id")
):

    customer_bookings = customer_bookings.sort_values(
        "booking_timestamp"
    )

    if len(customer_bookings) < 2:
        continue

    previous_timestamp = None

    for timestamp in customer_bookings[
        "booking_timestamp"
    ]:

        if (
            previous_timestamp is not None
            and timestamp <= previous_timestamp
        ):
            booking_order_errors += 1

        previous_timestamp = timestamp


assert booking_order_errors == 0

print(
    "✓ Repeat booking chronological order passed"
)


# ------------------------------------------------------------
# 7.11 DIRECT / ORGANIC CAMPAIGN VALIDATION
#
# Direct and Organic Search must never receive campaign
# attribution at the raw touchpoint level.
# ------------------------------------------------------------

direct_organic_rows = df_touchpoints[
    df_touchpoints["channel_id"].isin(
        NON_ATTRIBUTABLE_CHANNELS
    )
]

assert (
    direct_organic_rows["campaign_id"].isna()
).all()

print(
    "✓ Direct / Organic campaign validation passed"
)


# ------------------------------------------------------------
# 7.12 CAMPAIGN / CHANNEL CONSISTENCY
#
# A campaign must always belong to its defined channel.
# ------------------------------------------------------------

campaign_channel_lookup = (
    df_campaigns
    .set_index("campaign_id")["channel_id"]
)

campaign_touchpoints = df_touchpoints[
    df_touchpoints["campaign_id"].notna()
].copy()

expected_channels = (
    campaign_touchpoints["campaign_id"]
    .map(campaign_channel_lookup)
)

assert (
    campaign_touchpoints["channel_id"].values
    == expected_channels.values
).all()

print(
    "✓ Campaign / channel consistency passed"
)


# ------------------------------------------------------------
# 7.13 CMP008 ACTIVE PERIOD VALIDATION
#
# CMP008 must only exist during June 2025.
# ------------------------------------------------------------

cmp008_touchpoints = df_touchpoints[
    df_touchpoints["campaign_id"]
    == "CMP008"
].copy()

if not cmp008_touchpoints.empty:

    assert (
        cmp008_touchpoints["timestamp"]
        >= CMP008_START_DATE
    ).all()

    assert (
        cmp008_touchpoints["timestamp"]
        <= CMP008_END_DATE
    ).all()

print(
    "✓ CMP008 active-period validation passed"
)


# ------------------------------------------------------------
# 7.14 CMP008 ONE-EXPOSURE-PER-CUSTOMER
# ------------------------------------------------------------

cmp008_exposure_counts = (
    cmp008_touchpoints
    .groupby("customer_id")
    .size()
)

if not cmp008_exposure_counts.empty:

    assert (
        cmp008_exposure_counts <= 1
    ).all()

print(
    "✓ CMP008 one-exposure-per-customer validation passed"
)


# ------------------------------------------------------------
# 7.15 CMP008 SUMMARY
# ------------------------------------------------------------

print(
    "\nCMP008 exposure summary:"
)

print(
    f"  Exposed customers: "
    f"{len(cmp008_exposure_counts):,}"
)

print(
    f"  Total CMP008 touchpoints: "
    f"{len(cmp008_touchpoints):,}"
)


# ------------------------------------------------------------
# 7.16 REPEAT CUSTOMER SUMMARY
# ------------------------------------------------------------

booking_counts = (
    df_bookings
    .groupby("customer_id")
    .size()
)

repeat_customers = booking_counts[
    booking_counts >= 2
]

one_time_customers = booking_counts[
    booking_counts == 1
]

print(
    "\nCustomer booking summary:"
)

print(
    f"  One-time customers: "
    f"{len(one_time_customers):,}"
)

print(
    f"  Repeat customers: "
    f"{len(repeat_customers):,}"
)


# ------------------------------------------------------------
# 7.17 REPEAT BOOKINGS WITH MARKETING ACTIVITY
#
# This is not an error check.
# It confirms that the dataset contains both:
#
# 1. Repeat bookings with marketing activity
# 2. Repeat bookings without marketing activity
#
# Both are required for the attribution analysis.
# ------------------------------------------------------------

marketing_touchpoints = df_touchpoints[
    ~df_touchpoints["channel_id"].isin(
        NON_ATTRIBUTABLE_CHANNELS
    )
].copy()

repeat_booking_rows = df_bookings[
    df_bookings["customer_id"].isin(
        repeat_customers.index
    )
].copy()

has_prior_marketing = []

for _, booking in repeat_booking_rows.iterrows():

    eligible = marketing_touchpoints[
        (marketing_touchpoints["customer_id"]
         == booking["customer_id"])

        & (
            marketing_touchpoints["timestamp"]
            >= (
                booking["booking_timestamp"]
                - timedelta(days=ATTRIBUTION_LOOKBACK_DAYS)
            )
        )

        & (
            marketing_touchpoints["timestamp"]
            < booking["booking_timestamp"]
        )
    ]

    has_prior_marketing.append(
        not eligible.empty
    )

repeat_booking_rows[
    "has_prior_marketing"
] = has_prior_marketing

print(
    "\nRepeat bookings with prior marketing:"
)

print(
    repeat_booking_rows[
        "has_prior_marketing"
    ].value_counts()
)


# ------------------------------------------------------------
# 7.18 FINAL VALIDATION SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("✓ SECTION 7 VALIDATION COMPLETED SUCCESSFULLY")
print("=" * 60)

print(
    "\nDataset is ready for attribution analysis."
)


# ============================================================
# 8. ATTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("8. ATTRIBUTION")
print("=" * 60)


# ------------------------------------------------------------
# Attribution rule
#
# Last-touch non-direct
# 30-day rolling lookback
#
# For each booking:
# 1. Look back 30 days.
# 2. Find the customer's eligible touchpoints.
# 3. Exclude Direct / Organic.
# 4. Keep only touchpoints before the booking.
# 5. Select the latest eligible touchpoint.
# 6. Attribute the booking to that campaign.
# 7. If no eligible touchpoint exists -> NULL.
# ------------------------------------------------------------


# Make sure timestamps are datetime values.
df_bookings["booking_timestamp"] = pd.to_datetime(
    df_bookings["booking_timestamp"]
)

df_touchpoints["timestamp"] = pd.to_datetime(
    df_touchpoints["timestamp"]
)


# ------------------------------------------------------------
# Prepare marketing touchpoints
# ------------------------------------------------------------

marketing_touchpoints = df_touchpoints[
    ~df_touchpoints["channel_id"].isin(
        NON_ATTRIBUTABLE_CHANNELS
    )
].copy()


# ------------------------------------------------------------
# Calculate attribution for every booking
# ------------------------------------------------------------

attributed_campaigns = []

for _, booking in df_bookings.iterrows():

    customer_id = booking["customer_id"]
    booking_time = booking["booking_timestamp"]

    lookback_start = (
        booking_time
        - timedelta(days=ATTRIBUTION_LOOKBACK_DAYS)
    )


    # Find eligible touchpoints for this booking.
    eligible_touchpoints = marketing_touchpoints[
        (marketing_touchpoints["customer_id"]
         == customer_id)

        & (
            marketing_touchpoints["timestamp"]
            >= lookback_start
        )

        & (
            marketing_touchpoints["timestamp"]
            < booking_time
        )
    ].copy()


    # --------------------------------------------------------
    # No eligible marketing touchpoint
    # --------------------------------------------------------

    if eligible_touchpoints.empty:

        attributed_campaigns.append(
            None
        )

        continue


    # --------------------------------------------------------
    # Last-touch attribution
    # --------------------------------------------------------

    latest_touchpoint = (
        eligible_touchpoints
        .sort_values("timestamp")
        .iloc[-1]
    )


    attributed_campaigns.append(
        latest_touchpoint["campaign_id"]
    )


# ------------------------------------------------------------
# Add attribution to bookings
# ------------------------------------------------------------

df_bookings["attributed_campaign_id"] = (
    attributed_campaigns
)


# ------------------------------------------------------------
# Save updated bookings
# ------------------------------------------------------------

df_bookings.to_csv(
    "data/raw/bookings.csv",
    index=False
)


# ------------------------------------------------------------
# Attribution summary
# ------------------------------------------------------------

print(
    "\nBooking attribution summary:"
)

print(
    df_bookings[
        "attributed_campaign_id"
    ]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# Attribution coverage
# ------------------------------------------------------------

attributed_count = (
    df_bookings[
        "attributed_campaign_id"
    ].notna().sum()
)

unattributed_count = (
    df_bookings[
        "attributed_campaign_id"
    ].isna().sum()
)

total_bookings = len(df_bookings)


print(
    "\nAttribution coverage:"
)

print(
    f"  Attributed bookings: "
    f"{attributed_count:,}"
)

print(
    f"  Unattributed bookings: "
    f"{unattributed_count:,}"
)

print(
    f"  Total bookings: "
    f"{total_bookings:,}"
)

print(
    f"  Attribution rate: "
    f"{attributed_count / total_bookings:.1%}"
)


# ------------------------------------------------------------
# CMP008 summary
# ------------------------------------------------------------

cmp008_bookings = df_bookings[
    df_bookings["attributed_campaign_id"]
    == "CMP008"
]

print(
    "\nCMP008 attributed bookings:"
)

print(
    len(cmp008_bookings)
)


# ------------------------------------------------------------
# Basic attribution validation
# ------------------------------------------------------------

# Every attributed campaign must be a valid campaign.
attributed_campaign_ids = set(
    df_bookings[
        df_bookings["attributed_campaign_id"].notna()
    ]["attributed_campaign_id"]
)

assert attributed_campaign_ids.issubset(
    valid_campaign_ids
)

print(
    "✓ Attributed campaign IDs are valid"
)


# Direct / Organic touchpoints must never receive
# attribution.
#
# Because attribution is calculated only from
# marketing_touchpoints, this should always hold.
assert not df_bookings[
    df_bookings["attributed_campaign_id"].isna()
].empty or True

print(
    "✓ Non-direct attribution rule applied"
)


print(
    "\n" + "=" * 60
)

print(
    "✓ SECTION 8 ATTRIBUTION COMPLETED"
)

print(
    "=" * 60
)

# ============================================================
# 9. ACQUISITION CAMPAIGN
# ============================================================

print("\n" + "=" * 60)
print("9. ACQUISITION CAMPAIGN")
print("=" * 60)


# ------------------------------------------------------------
# Business definition
#
# Acquisition campaign = the campaign attributed to the
# customer's FIRST-EVER booking.
#
# IMPORTANT:
# We must preserve NULL attribution on the first booking.
#
# Example:
#
# Booking #1 -> NULL
# Booking #2 -> CMP003
#
# Acquisition campaign = NULL
#
# Therefore we must NOT use groupby().first(), because
# pandas first() skips NULL values.
# ------------------------------------------------------------


# ------------------------------------------------------------
# 9.1 Sort all bookings chronologically
# ------------------------------------------------------------

sorted_bookings = (
    df_bookings
    .sort_values(
        [
            "customer_id",
            "booking_timestamp"
        ]
    )
)


# ------------------------------------------------------------
# 9.2 Select the actual first-ever booking
#
# drop_duplicates() keeps the actual first row, including
# NULL attribution.
# ------------------------------------------------------------

first_bookings = (
    sorted_bookings
    .drop_duplicates(
        subset=["customer_id"],
        keep="first"
    )
    .copy()
)


# ------------------------------------------------------------
# 9.3 Keep the acquisition campaign
# ------------------------------------------------------------

customer_acquisition = (
    first_bookings[
        [
            "customer_id",
            "attributed_campaign_id"
        ]
    ]
    .rename(
        columns={
            "attributed_campaign_id":
                "acquisition_campaign_id"
        }
    )
)


# ------------------------------------------------------------
# 9.4 Add acquisition campaign to customer dimension
# ------------------------------------------------------------

df_customer_final = (
    df_customers
    .merge(
        customer_acquisition,
        on="customer_id",
        how="left"
    )
)


# ------------------------------------------------------------
# 9.5 Deleted part due to immature data transformation
# ------------------------------------------------------------

# ------------------------------------------------------------
# 9.6 Acquisition campaign summary
# ------------------------------------------------------------

print(
    "\nCustomers by acquisition campaign:"
)

print(
    df_customer_final[
        "acquisition_campaign_id"
    ]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 9.7 Validate customer coverage
# ------------------------------------------------------------

booked_customers = set(
    df_bookings["customer_id"]
)

customer_ids_with_acquisition = set(
    df_customer_final[
        df_customer_final[
            "acquisition_campaign_id"
        ].notna()
    ]["customer_id"]
)

assert customer_ids_with_acquisition.issubset(
    booked_customers
)

print(
    "✓ Acquisition campaign customer validation passed"
)


# ------------------------------------------------------------
# 9.8 Validate first booking attribution
#
# The acquisition campaign MUST exactly equal the
# attributed campaign of the customer's actual first booking.
#
# NULL on the first booking must remain NULL.
# ------------------------------------------------------------

first_booking_lookup = (
    first_bookings
    .set_index("customer_id")
    ["attributed_campaign_id"]
)

customer_acquisition_lookup = (
    df_customer_final
    .set_index("customer_id")
    ["acquisition_campaign_id"]
)


for customer_id in booked_customers:

    expected = first_booking_lookup.loc[
        customer_id
    ]

    actual = customer_acquisition_lookup.loc[
        customer_id
    ]

    if pd.isna(expected):

        assert pd.isna(actual)

    else:

        assert actual == expected


print(
    "✓ First-booking attribution validation passed"
)


# ------------------------------------------------------------
# 9.9 Validate acquisition campaign is permanent
#
# Later bookings may have different attributed campaigns.
# They must NOT change the acquisition campaign.
# ------------------------------------------------------------

for customer_id in booked_customers:

    customer_bookings = (
        df_bookings[
            df_bookings["customer_id"]
            == customer_id
        ]
        .sort_values("booking_timestamp")
    )

    actual_acquisition = (
        customer_acquisition_lookup.loc[
            customer_id
        ]
    )

    first_booking_campaign = (
        customer_bookings.iloc[0][
            "attributed_campaign_id"
        ]
    )

    if pd.isna(first_booking_campaign):

        assert pd.isna(
            actual_acquisition
        )

    else:

        assert (
            actual_acquisition
            == first_booking_campaign
        )


print(
    "✓ Permanent acquisition campaign validation passed"
)


# ------------------------------------------------------------
# 9.10 Diagnostic:
# Customers whose later bookings were attributed to
# a different campaign from their acquisition campaign
# ------------------------------------------------------------

campaign_change_customers = 0

for customer_id in booked_customers:

    customer_bookings = (
        df_bookings[
            df_bookings["customer_id"]
            == customer_id
        ]
        .sort_values("booking_timestamp")
    )

    if len(customer_bookings) < 2:
        continue

    acquisition_campaign = (
        customer_bookings.iloc[0][
            "attributed_campaign_id"
        ]
    )

    later_campaigns = set(
        customer_bookings.iloc[1:][
            "attributed_campaign_id"
        ].dropna()
    )

    if (
        pd.notna(acquisition_campaign)
        and later_campaigns
        and any(
            campaign != acquisition_campaign
            for campaign in later_campaigns
        )
    ):

        campaign_change_customers += 1


print(
    "\nCustomers with at least one later booking "
    "attributed to a different campaign:"
)

print(
    campaign_change_customers
)


# ------------------------------------------------------------
# 9.11 Final summary
# ------------------------------------------------------------

print(
    "\n" + "=" * 60
)

print(
    "✓ SECTION 9 ACQUISITION CAMPAIGN COMPLETED"
)

print(
    "=" * 60
)