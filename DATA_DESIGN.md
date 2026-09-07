# Data Design

## 1. Purpose

This document describes the design principles, data relationships, customer journey logic, attribution rules, and intentional analytical scenarios used to generate the synthetic OTA marketing dataset.

The dataset is designed specifically for a portfolio project that demonstrates how marketing analytics, data modeling, SQL, data engineering practices, and business reasoning can work together.

The objective is not to reproduce a real company's data exactly.

Instead, the objective is to create a synthetic environment with realistic relationships and analytical edge cases that allow meaningful marketing and commercial questions to be investigated.

---

## 2. Design Philosophy

### Business questions drive data complexity

The synthetic data was deliberately designed around the questions the portfolio needs to answer.

A basic independently generated dataset could demonstrate:

* CSV ingestion
* SQL queries
* aggregations
* joins
* basic marketing metrics

However, it would not reliably support more advanced questions about:

* acquisition quality
* repeat bookings
* customer value
* cross-campaign re-engagement
* attribution
* incremental performance
* marketing profitability

For this reason, the dataset is generated from customer journeys first rather than generating each table independently.

The core principle is:

```text
Business questions
       ↓
Customer journey design
       ↓
Related data generation
       ↓
Data model
       ↓
Analytical pipeline
       ↓
Business analysis
```

This approach intentionally adds complexity where that complexity creates analytical value.

---

## 3. Customer-Journey-First Generation

The generator first establishes customer behavior and journeys.

Records such as marketing touchpoints and bookings are then generated based on those journeys.

Conceptually:

```text
Customer profile
      ↓
Customer journey
      ↓
Marketing touchpoints
      ↓
Bookings
      ↓
Booking attribution
      ↓
Acquisition attribution
```

This ensures that relationships between tables are meaningful rather than coincidental.

For example, a repeat booking can be associated with a different campaign from the campaign that originally acquired the customer.

This would be difficult to represent consistently if customers, bookings, and touchpoints were generated independently.

---

## 4. Data Model

The project uses a dimensional-style analytical model consisting of dimensions and fact tables.

### Dimension tables

| Table          | Grain              | Purpose                                         |
| -------------- | ------------------ | ----------------------------------------------- |
| `dim_customer` | 1 row per customer | Customer attributes and acquisition information |
| `dim_campaign` | 1 row per campaign | Campaign attributes and channel relationship    |
| `dim_channel`  | 1 row per channel  | Marketing channel definitions                   |
| `dim_date`     | 1 row per date     | Consistent date analysis                        |

### Fact tables

| Table                       | Grain                      | Purpose                                            |
| --------------------------- | -------------------------- | -------------------------------------------------- |
| `fact_marketing_touchpoint` | 1 row per touchpoint       | Customer interactions with marketing activity      |
| `fact_booking`              | 1 row per booking          | Booking transactions and booking-level attribution |
| `fact_ad_performance`       | 1 row per campaign per day | Campaign delivery, clicks, and spend               |

The grain of each table is intentionally defined so that downstream joins and aggregations can be controlled.

---

## 5. Data Layers and Modeling Approach

The project separates source-style data ingestion from analytical transformation and modeling.

```text
data/raw/

    ↓

Python ingestion & validation

    ↓

DuckDB source tables

    ↓

SQL transformations / analytical models

    ↓

Business analysis
```

### Raw layer

The raw layer represents source-style datasets generated to simulate data from an OTA environment:

* `customers.csv`
* `channels.csv`
* `campaigns.csv`
* `touchpoints.csv`
* `bookings.csv`
* `ad_performance.csv`

These datasets are treated as the source data for the local analytical pipeline.

### Ingestion layer

`src/ingest_data.py` loads the raw CSV datasets into DuckDB and performs basic structural and business-value validation, including primary-key, foreign-key, grain, and value checks.

The resulting DuckDB tables represent the ingested source data and provide the foundation for downstream analysis.

### Transformation and analytical modeling

Analytical transformations are performed in DuckDB using SQL rather than during synthetic data generation.

A transformed dataset will be materialized as an analytical model when it represents a useful reusable business concept. For simpler analyses, SQL queries and CTEs may be used directly without creating an additional physical model.

This separation keeps the responsibilities of the project clear:

* `generate_data.py` → generates synthetic source data
* `ingest_data.py` → ingests and validates source data
* SQL → transforms and models data for analytical use
* Analytical queries → answer business questions and generate insights

This approach allows the project to demonstrate both practical data engineering and analytical capabilities without mixing synthetic data generation with downstream data transformation.


---

## 6. Customer Acquisition

Acquisition campaign is a customer-level concept.

For each customer, the acquisition campaign is determined from the campaign attributed to the customer's first-ever booking.

Once established, the acquisition campaign does not change.

For example:

```text
Customer A

Campaign A → Booking 1
              ↑
       acquisition campaign

Campaign B → Booking 2
Campaign C → Booking 3
```

Customer A remains an acquisition customer of Campaign A even though later bookings may be attributed to Campaign B or Campaign C.

This distinction allows the project to separately analyze:

* customer acquisition
* subsequent re-engagement
* repeat booking behavior
* customer quality by acquisition source

---

## 7. Booking-Level Attribution

Acquisition campaign and booking attribution are intentionally separate concepts.

Every booking is evaluated independently for marketing attribution.

A repeat booking may therefore have a different attributed campaign from the customer's original acquisition campaign.

Example:

```text
Campaign A → Booking 1
                ↓
        Customer acquired by A

Campaign B → Campaign C → Booking 2
                            ↑
                   Booking attributed to C
```

The customer remains acquired by Campaign A, while Booking 2 is attributed to Campaign C.

This allows cross-campaign customer journeys to be analyzed without changing the customer's original acquisition cohort.

---

## 8. Attribution Rules

The project uses a **last-touch non-direct attribution model with a 30-day lookback window**.

For each booking:

1. Look back 30 days from the booking timestamp.
2. Consider marketing touchpoints within that window.
3. Exclude Direct and Organic touchpoints from campaign attribution.
4. Select the latest eligible non-direct marketing touchpoint.
5. Assign that touchpoint's campaign to the booking.
6. If no eligible marketing touchpoint exists, the booking receives `NULL` campaign attribution.

Conceptually:

```text
Touchpoint A
     ↓
Touchpoint B
     ↓
Booking
     ↑
Latest eligible non-direct touchpoint
```

### Direct and Organic behavior

Direct and Organic interactions can occur in the customer journey, but they are not eligible to receive campaign attribution.

For example:

```text
Campaign A
    ↓
Direct
    ↓
Booking
```

The booking can still be attributed to Campaign A if the Campaign A touchpoint is within the 30-day lookback window.

The presence of a Direct interaction does not automatically erase an eligible prior marketing touchpoint.

### Attribution expiry

If the latest eligible marketing touchpoint is more than 30 days before the booking, it cannot receive attribution.

Example:

```text
Campaign A → Booking 1
                    ↓
              45 days later
                    ↓
                 Booking 2

Booking 2 attribution = NULL
```

unless another eligible marketing touchpoint occurs within the relevant 30-day window.

### Attribution journey reset

Each completed booking ends the current attribution journey.

The next booking starts a new attribution evaluation using the same 30-day lookback rule.

This prevents one booking from permanently influencing every future booking made by the customer.

---

## 9. Repeat Customer Design

Customers are intentionally divided into different behavioral patterns.

Some customers:

* make only one booking
* return once
* return multiple times
* return after different marketing interactions
* return without a new attributable marketing touchpoint

This creates a more useful basis for analyzing customer quality.

The dataset therefore supports questions such as:

> Are campaigns acquiring customers who come back?

and:

> Does acquisition volume translate into valuable customers?

Repeat booking intervals are also intentionally varied rather than using a single fixed interval.

---

## 10. Cross-Campaign Customer Journeys

Customers can interact with multiple campaigns over their lifetime.

A simplified example:

```text
Customer
   ↓
CMP001
   ↓
CMP002
   ↓
Booking #1 → attributed to CMP002
   ↓
CMP003
   ↓
CMP001
   ↓
Booking #2 → attributed to CMP001
```

This behavior is intentional.

It allows the analysis to distinguish between:

* the campaign that originally acquired the customer
* campaigns that later re-engaged the customer
* the campaign receiving attribution for an individual booking

This is important when evaluating acquisition quality and lifecycle marketing.

---

## 11. Direct and Organic Bookings

Not every booking should have campaign attribution.

Some customers can book without a qualifying non-direct marketing touchpoint.

These bookings receive:

```text
attributed_campaign_id = NULL
```

This is intentional because a marketing dataset in which every booking is automatically assigned to a campaign would make attribution unrealistically clean.

Unattributed bookings provide a useful comparison group and help prevent the analysis from assuming that all business outcomes are caused by measurable campaign activity.

---

## 12. Campaign Design

Campaigns are intentionally differentiated.

The synthetic campaigns do not all have the same:

* impression volume
* click-through rate
* cost
* acquisition volume
* customer quality

This prevents campaign performance from becoming artificially uniform.

The intended analytical environment includes campaigns that can be:

* high volume
* high quality
* highly efficient
* relatively expensive
* lower volume but valuable
* strong in acquisition but weaker in customer quality

This creates trade-offs that can be evaluated rather than producing an obvious single “best” campaign.

---

## 13. Seasonality

Campaign activity includes moderate seasonal variation.

The purpose is to prevent campaign performance from being completely flat throughout the year while avoiding unnecessary complexity.

Higher activity is introduced during selected travel-demand periods, while other periods have lower activity.

This allows later analysis to consider the possibility that campaign performance differences may partly reflect seasonality rather than campaign strategy alone.

---

## 14. Intentional Attribution-Quality Challenge: CMP008

One campaign, `CMP008` (`Weekend Getaway`), is intentionally designed as an analytical challenge.

The campaign behaves like a normal campaign in the raw data.

The data does not label it as fraudulent.

Its unusual behavior is intended to be discovered through analysis.

### Active period

CMP008 runs for one month:

```text
June 1, 2025 → June 30, 2025
```

It is then discontinued.

### Exposure behavior

During the active period:

* CMP008 has unusually high impressions.
* Exposed customers receive exactly one CMP008 touchpoint.
* A customer cannot receive repeated CMP008 exposures.
* The audience is disproportionately composed of high-intent users.
* Some exposed users do not book.
* Some exposed users have other interactions before booking.

### Why this matters

The campaign is designed to exploit a weakness in last-touch attribution.

Consider:

```text
Direct / Organic
       ↓
   CMP008
       ↓
    Booking
```

Under the project's last-touch non-direct attribution model, CMP008 receives credit for the booking.

However, the user's underlying intent may already have existed before the CMP008 exposure.

Therefore:

```text
Reported attribution
        ≠
Incremental business impact
```

The campaign can appear highly effective based on attributed conversions and CPA while primarily shifting credit away from Direct/Organic activity.

### Stable conversion-volume principle

The fraud scenario is designed so that overall conversion volume remains approximately stable during the active period.

Conceptually:

```text
Before:

Direct = 100
CMP008 = 0
Total = 100


During CMP008:

Direct = 40
CMP008 = 60
Total = 100
```

The exact numbers are not fixed; the important design principle is that CMP008 should primarily **capture attribution credit rather than create a large artificial increase in total bookings**.

This creates a realistic analytical question:

> Is the campaign generating incremental conversions, or is it simply receiving credit for conversions that were likely to happen anyway?

This scenario will later be investigated through the marketing performance analysis.

---

## 15. Booking Value Design

Booking values are intentionally skewed rather than uniformly distributed.

Most bookings have moderate values, while some bookings have higher values and a small number have very high values.

This better represents the long-tail behavior often found in transaction data.

The design supports analysis of:

* booking revenue
* average booking value
* customer value
* acquisition revenue
* repeat customer value
* campaign-level revenue
* profitability

It also prevents revenue analysis from being dominated by an unrealistic uniform transaction value.

---

## 16. Marketing Touchpoint Design

Not every marketing touchpoint results in a booking.

The dataset intentionally includes:

* customers with no touchpoints
* customers with touchpoints but no booking
* customers with one booking
* customers with repeat bookings
* touchpoints that occur before bookings
* touchpoints that fall outside attribution windows

This allows marketing performance to be analyzed as a customer journey rather than as a simple:

```text
Campaign → Booking
```

relationship.

---

## 17. Ad Performance Design

Campaign advertising performance is generated at:

```text
1 campaign × 1 day
```

The dataset includes:

* impressions
* clicks
* spend

Campaigns have different performance profiles, and daily values include moderate variation.

The data also incorporates seasonality.

This creates a foundation for calculating metrics such as:

* CTR
* CPC
* CPA / CAC
* ROAS
* revenue per campaign
* spend efficiency

The ad-performance data is intentionally separate from customer touchpoints because advertising delivery metrics and customer-level interactions represent different grains.

---

## 18. Data Quality and Validation

The generated data is validated before being used for analysis.

Validation covers areas including:

### Primary-key integrity

Expected unique identifiers are checked for duplicates and missing values.

### Composite grain integrity

Campaign-day ad performance is validated using:

```text
campaign_id + date
```

as its composite key.

### Foreign-key integrity

Relationships between customers, campaigns, channels, bookings, touchpoints, and ad performance are validated.

### Business-value constraints

The generator checks for invalid values such as:

* negative booking values
* negative spend
* non-positive impressions
* clicks greater than impressions

### Timeline consistency

The generated data is checked to ensure:

* bookings occur after customer signup
* touchpoints occur after signup
* touchpoints used for attribution occur before the booking
* repeat bookings occur chronologically
* CMP008 activity stays within its defined active period

### Special-case validation

The intentional CMP008 behavior is also validated, including:

* active-period restrictions
* one exposure per customer
* attribution behavior

The purpose of validation is to ensure that the synthetic complexity remains controlled and analytically usable.

---

## 19. Analytical Questions Enabled

The resulting dataset supports several connected analytical questions.

### Customer Acquisition

* How many customers does each campaign acquire?
* Which campaigns drive first-time customers?
* How does acquisition volume differ by campaign?

### Acquisition Quality

* Which campaigns acquire customers who return?
* Which acquisition cohorts generate higher booking value?
* Does acquisition volume correlate with customer quality?

### Re-engagement

* Which campaigns receive attribution for repeat bookings?
* Do customers move between campaigns over their lifecycle?
* How frequently do repeat bookings occur without attributable marketing?

### Marketing Efficiency

* Which campaigns have the best CTR?
* Which campaigns have the best CPC?
* Which campaigns have the best CPA/CAC?
* Which campaigns generate the strongest ROAS?

### Attribution Quality

* Are attributed conversions necessarily incremental?
* Does campaign performance change when compared with overall booking volume?
* Can attribution be captured without materially increasing total conversions?
* What evidence suggests that CMP008 is receiving credit for existing intent?

### Profitability

* Which campaigns generate revenue relative to spend?
* Does efficient acquisition also produce valuable customers?
* Which campaigns appear attractive from a volume perspective but weaker from a commercial perspective?

These questions form the foundation for the portfolio's later SQL analysis, dashboard, and business recommendations.

---

## 20. Design Principle Summary

The central design principle is:

> **Synthetic data should be complex because the business question requires it, not because complexity itself is valuable.**

The additional complexity in this dataset exists to preserve relationships that are necessary for meaningful analysis.

The resulting project therefore connects:

```text
Synthetic data design
        ↓
Data ingestion
        ↓
Data validation
        ↓
Data modeling
        ↓
SQL analysis
        ↓
Marketing metrics
        ↓
Business interpretation
        ↓
Recommendations
```

This makes the synthetic dataset part of the analytical solution rather than simply sample data used to demonstrate SQL syntax.
