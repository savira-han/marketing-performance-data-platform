# Marketing Performance Data Platform

An end-to-end marketing analytics and data platform for evaluating **customer acquisition, campaign economics, customer quality, booking growth, and attribution reliability** across a 2025 travel marketplace.

The analysis connects marketing touchpoints, customer acquisition, advertising performance, booking behavior, and campaign attribution to answer a broader business question:

> **Which marketing activities are generating valuable customers efficiently, how is customer behavior contributing to growth, and how much confidence should be placed in reported campaign performance?**

### Analysis Scope

| Metric                  |        Value |
| ----------------------- | -----------: |
| Customers Reached       |        8,456 |
| Customers with Bookings |        5,456 |
| Total Bookings          |        9,140 |
| Marketing Touchpoints   |       40,890 |
| Analysis Period         | Jan–Dec 2025 |

---

# Executive Summary

### Acquisition

**Paid marketing is the primary acquisition engine.**

4,638 of 5,456 customers with bookings were acquired through paid campaigns, representing **85.01%** of acquired customers.

### Campaign Economics

**Brand Search and Hotel Deals show the strongest acquisition economics among the normal campaigns.**

Brand Search combines the largest acquisition volume with the lowest CAC and highest first-booking ROAS. Hotel Deals shows similarly strong efficiency and the highest average first-booking value.

### Customer Quality

**Customer booking-frequency distributions are broadly similar across major campaigns.**

Approximately 62–65% of acquired customers made one booking, while repeat and frequent customer proportions remained relatively consistent.

Observed monetary value provides more differentiation than booking frequency alone.

### Growth

**Repeat customers became an increasingly important contributor to booking volume during 2025.**

Repeat bookings represented 2.00% of January bookings and approximately 45–48% during much of the second half of the year.

### Attribution

**CMP008 presents an attribution-quality signal that warrants investigation.**

36 of 38 bookings attributed to CMP008 came from customers who had already been exposed to other marketing.

The pattern is unusual, but the available data does not establish that CMP008 stole attribution or generated no incremental demand.

### Decision Principle

> **Scale demonstrated economics, optimize weaker economics, validate promising signals, and investigate measurement anomalies before increasing investment.**

---

# 01 — Customer Acquisition & Campaign Economics

## Acquisition Sources

In 2025, 5,456 customers made at least one booking.

| Acquisition Source              | Customers |    Share |
| ------------------------------- | --------: | -------: |
| Paid Campaign                   |     4,638 |   85.01% |
| Organic / Direct / Unattributed |       818 |   14.99% |
| **Total**                       | **5,456** | **100%** |

Paid marketing therefore represents the primary customer acquisition engine.

The Organic / Direct / Unattributed group should not be interpreted as purely organic acquisition. It includes customers whose first booking did not receive attribution from an eligible non-direct marketing campaign under the defined attribution rules.

---

## Campaign Economics

Campaign performance is evaluated using:

* Acquired customers
* Advertising spend
* Customer acquisition cost (CAC)
* First-booking ROAS
* Average first-booking value

| Campaign           | Acquired | Acquisition Share |     CAC |  ROAS | Avg. First Booking |
| ------------------ | -------: | ----------------: | ------: | ----: | -----------------: |
| Brand Search       |    1,146 |            24.71% |  $73.12 | 4.85x |            $354.52 |
| Hotel Deals        |      931 |            20.07% |  $79.31 | 4.84x |            $383.86 |
| Generic Search     |    1,137 |            24.52% | $100.51 | 3.65x |            $366.91 |
| Summer Sale        |      946 |            20.39% | $101.17 | 3.67x |            $370.94 |
| Travel Inspiration |      458 |             9.87% |  $95.84 | 3.81x |            $365.19 |

### Assessment

**Brand Search** combines the largest acquisition volume with the lowest CAC and highest first-booking ROAS.

**Hotel Deals** demonstrates similarly strong acquisition efficiency and the highest average first-booking value among the normal campaigns.

**Generic Search** and **Summer Sale** provide meaningful acquisition scale but operate at higher CAC and lower ROAS.

**Travel Inspiration** has weaker acquisition economics but shows an interesting downstream customer-value signal requiring further validation.

> **Measurement note:** ROAS is calculated as first-booking value divided by advertising spend. It does not represent profit or full customer lifetime value.

---

## Conversion Rate Context

Observed conversion rates are relatively close across the major campaigns:

| Campaign           | Reached | Converted | Conversion |
| ------------------ | ------: | --------: | ---------: |
| Brand Search       |   4,449 |     3,186 |     71.61% |
| Generic Search     |   4,355 |     3,178 |     72.97% |
| Summer Sale        |   3,930 |     2,874 |     73.13% |
| Hotel Deals        |   3,952 |     2,868 |     72.57% |
| Travel Inspiration |   2,276 |     1,730 |     76.01% |

This indicates that observed conversion rate is not the primary differentiator among the normal campaigns.

The more meaningful differences are in:

* Acquisition cost
* Acquisition scale
* First-booking value
* Downstream customer value

---

# 02 — Customer Quality

## Customer Behavior

Customers are segmented according to observed booking frequency:

* **One-time:** 1 booking
* **Repeat:** 2 bookings
* **Frequent:** 3+ bookings

| Segment  | Customers | Share |
| -------- | --------: | ----: |
| One-time |     3,443 | 63.1% |
| Repeat   |       847 | 15.5% |
| Frequent |     1,166 | 21.4% |

Across the major campaigns:

| Campaign           | One-time | Repeat | Frequent |
| ------------------ | -------: | -----: | -------: |
| Brand Search       |    61.7% |  16.7% |    21.6% |
| Generic Search     |    62.4% |  16.5% |    21.2% |
| Summer Sale        |    64.3% |  14.6% |    21.1% |
| Hotel Deals        |    63.8% |  14.9% |    21.3% |
| Travel Inspiration |    64.6% |  15.9% |    19.4% |

### Assessment

The customer mix is relatively consistent across campaigns.

There is no strong evidence that the major campaigns acquire fundamentally different customers when evaluated using booking frequency alone.

---

## Observed Customer Value

### Repeat Customers

| Campaign           | Avg. Customer Value |
| ------------------ | ------------------: |
| Hotel Deals        |                $791 |
| Generic Search     |                $748 |
| Brand Search       |                $722 |
| Travel Inspiration |                $708 |
| Summer Sale        |                $664 |

### Frequent Customers

| Campaign           | Avg. Customer Value |
| ------------------ | ------------------: |
| Travel Inspiration |              $1,327 |
| Brand Search       |              $1,319 |
| Generic Search     |              $1,265 |
| Summer Sale        |              $1,238 |
| Hotel Deals        |              $1,233 |

### Assessment

Customer quality should not be evaluated using booking frequency alone.

Travel Inspiration, for example, has the lowest frequent-customer share among the major campaigns but the highest observed value among frequent customers.

These values should be interpreted directionally rather than as full LTV because customers acquired earlier in the year have more opportunity to generate additional bookings.

---

# 03 — Booking Growth

## New vs. Repeat Bookings

The customer base generated:

* 8,456 customers reached
* 5,456 customers with bookings
* 9,140 total bookings
* 1.68 bookings per converted customer

Monthly booking composition changed substantially throughout the year.

| Month | New Bookings | Repeat Bookings | Total | Repeat Share |
| ----- | -----------: | --------------: | ----: | -----------: |
| Jan   |           98 |               2 |   100 |        2.00% |
| Mar   |          531 |             137 |   668 |       20.51% |
| Jun   |          490 |             345 |   835 |       41.32% |
| Sep   |          506 |             433 |   939 |       46.11% |
| Oct   |          469 |             431 |   900 |       47.89% |
| Dec   |          521 |             424 |   945 |       44.87% |

### Assessment

Repeat bookings increased from **2.00% of January bookings** to roughly **45–48% during much of the second half of the year**.

This establishes that existing customers became an increasingly important contributor to booking volume.

It does **not**, however, establish that retention improved. The existing customer base naturally accumulates over time.

### Business Implication

Growth should not be viewed purely as a customer acquisition problem.

Customer lifecycle activity — including rebooking, engagement, and customer value — is an increasingly important component of the growth strategy.

---

# 04 — Attribution Integrity

## Attribution Methodology

Campaign attribution uses:

* **Last-touch attribution**
* **Non-direct marketing touchpoints**
* **30-day lookback window**

For each booking, the most recent eligible marketing touchpoint within the preceding 30 days receives attribution credit.

```text
Customer Touchpoints
        ↓
30-Day Lookback
        ↓
Exclude Direct / Organic
        ↓
Most Recent Eligible Marketing Touchpoint
        ↓
Attributed Campaign
```

The methodology answers:

> Which eligible marketing touchpoint receives reporting credit?

It does **not** answer:

> Would the booking have happened without the campaign?

Therefore:

> **Attributed booking ≠ proven incremental booking**

This distinction is critical when campaign attribution is used to support investment decisions.

---

## CMP008 Investigation

CMP008 — Weekend Getaway — presents an unusual attribution pattern.

| Metric                                            | Observation |
| ------------------------------------------------- | ----------: |
| Customers Reached                                 |         132 |
| Customers Subsequently Booking                    |         118 |
| Observed Conversion                               |      89.39% |
| Attributed Bookings                               |          38 |
| Attributed Bookings with Prior Marketing Exposure |          36 |
| Prior Marketing Exposure Rate                     |      94.74% |

The combination of:

* unusually high observed conversion
* limited reach
* short campaign duration
* high prior marketing exposure

makes CMP008 an attribution-quality signal worth investigating.

### What the Data Supports

The pattern is unusual enough to warrant investigation.

### What the Data Does Not Establish

The analysis does not establish that CMP008:

* stole attribution from another campaign
* caused the bookings
* generated no incremental demand
* displaced another campaign

Those conclusions require causal evidence.

### Business Treatment

CMP008 is therefore:

1. Excluded from the primary campaign benchmark.
2. Not used as evidence for scaling.
3. Treated as an attribution investigation case.

A randomized holdout, geo-based experiment, or other appropriate causal design would be required to establish incremental impact.

---

# 05 — Business Recommendations

## Campaign Investment

| Campaign               | Recommended Action              | Rationale                                                                         |
| ---------------------- | ------------------------------- | --------------------------------------------------------------------------------- |
| **Brand Search**       | Continue / consider scaling     | Strongest combination of scale, CAC, ROAS, and observed customer value            |
| **Hotel Deals**        | Continue / investment candidate | Strong CAC and ROAS with high first-booking and repeat-customer value             |
| **Generic Search**     | Optimize before scaling         | Meaningful scale but materially weaker CAC and ROAS                               |
| **Summer Sale**        | Review and optimize             | Meaningful scale but weaker acquisition economics and lower repeat-customer value |
| **Travel Inspiration** | Validate before scaling         | Promising frequent-customer value signal despite weaker acquisition efficiency    |
| **CMP008**             | Investigate separately          | Unusual attribution pattern and insufficient evidence for normal benchmarking     |

Scaling decisions should also consider **marginal CAC and incrementality** rather than assuming historical campaign economics will remain constant as spend increases.

---

## Growth Priorities

### 1. Acquire Efficiently

Paid campaigns represent 85.01% of acquired customers.

Investment should prioritize campaigns that demonstrate strong economics at sufficient scale.

### 2. Increase Value From Existing Customers

Repeat bookings became an increasingly important contributor to booking volume.

Relevant areas for further optimization include:

* Customer lifecycle segmentation
* Rebooking campaigns
* Personalized offers
* Post-booking engagement
* Cohort-based customer value measurement

### 3. Improve Measurement Confidence

Campaign reporting should distinguish between:

```text
Observed Attribution
        ≠
Incremental Business Impact
```

Attribution remains useful for performance reporting, but investment decisions should incorporate measurement confidence.

---

# 06 — Analytical Limitations

## Supported by the Analysis

The data supports conclusions about:

* Campaign acquisition volume
* Acquisition share
* CAC
* First-booking ROAS
* Customer booking-frequency segments
* Observed customer booking value
* Booking growth composition
* Attribution assignments under the defined model
* Unusual attribution patterns

## Not Established by the Analysis

The analysis does not establish:

* True campaign profitability
* Incremental revenue
* Causal campaign impact
* Complete customer lifetime value
* Causal differences in retention between campaigns
* Whether CMP008 displaced or stole attribution
* Whether CMP008 generated incremental demand

These limitations define the appropriate confidence level for each business decision.

---

# 07 — Data & Technical Architecture

The analytical environment connects data generation, ingestion, storage, transformation, analysis, and presentation.

```text
Python Data Generation
        ↓
Synthetic CSV Data
        ↓
Python Ingestion
        ↓
DuckDB
        ↓
SQL Transformations
        ↓
Analytical Queries
        ↓
Streamlit
```

The separation between data generation, ingestion, analytical transformations, and presentation allows the underlying data to be regenerated while keeping the analytical logic reusable.

---

## Data Layer

Synthetic marketing, customer, touchpoint, campaign, advertising, and booking data are generated using Python.

The generated source data is ingested into DuckDB for analytical processing.

### Core Tables

* `customers`
* `touchpoints`
* `bookings`
* `campaigns`
* `channels`
* `ad_performance`
* `customer_first_booking`
* `acquired_customer_behavior`

---

## Analytical Layer

SQL is used as the primary language for analytical transformations and business logic.

Core analytical models include:

* `customer_first_booking.sql`
* `acquired_customer_behavior.sql`

Core analytical queries include:

* `customer_acquisition.sql`
* `customer_quality.sql`
* `funnel_growth.sql`
* `attribution_prior_activity.sql`

The analytical layer is kept separate from the presentation layer so that business logic can be reused independently of the dashboard.

---

## Pipeline

The data pipeline runs through:

```bash
python run_pipeline.py
```

The workflow is:

```text
generate_data.py
        ↓
ingest_data.py
        ↓
DuckDB
```

Analytical SQL then operates on the resulting database.

---

# 08 — Repository Structure

```text
marketing-performance-data-platform/
│
├── data/
│   └── raw/
│
├── models/
│   ├── customer_first_booking.sql
│   └── acquired_customer_behavior.sql
│
├── queries/
│   ├── customer_acquisition.sql
│   ├── customer_quality.sql
│   ├── funnel_growth.sql
│   └── attribution_prior_activity.sql
│
├── src/
│   ├── generate_data.py
│   └── ingest_data.py
│
├── app.py
├── run_pipeline.py
├── build_tables.py
├── query.py
├── query_to_csv.py
├── DATA_DESIGN.md
└── README.md
```

### Key Components

| Component              | Purpose                                          |
| ---------------------- | ------------------------------------------------ |
| `src/generate_data.py` | Generates synthetic source data                  |
| `src/ingest_data.py`   | Loads generated data into DuckDB                 |
| `run_pipeline.py`      | Runs the data generation and ingestion workflow  |
| `models/`              | Reusable SQL transformations                     |
| `queries/`             | Analytical queries and business logic            |
| `app.py`               | Streamlit presentation layer                     |
| `build_tables.py`      | DuckDB table-building and analytical development |
| `query.py`             | Utility for running analytical SQL               |
| `query_to_csv.py`      | Utility for exporting analytical results         |
| `DATA_DESIGN.md`       | Data model and analytical design documentation   |

---

# 09 — Analytical Environment

### Technologies

* **Python** — data generation, ingestion, and pipeline execution
* **SQL** — analytical transformations and business logic
* **DuckDB** — local analytical database
* **Streamlit** — interactive analytical presentation
* **Git / GitHub** — version control

### Data Characteristics

The analytical environment contains:

* **40,890** marketing touchpoints
* **8,456** customers reached
* **5,456** customers with bookings
* **9,140** bookings
* Booking activity across **January–December 2025**

The environment includes realistic customer journeys, cross-campaign exposure, direct and organic interactions, repeat bookings, campaign performance differences, and attribution-quality anomalies.

---

# 10 — Data Governance & Interpretation

All data used in the analysis is synthetic.

The environment is designed to represent a realistic OTA marketing analytics workflow without exposing real customer, transaction, advertising, or company data.

The synthetic data supports analysis of:

* Customer acquisition
* Campaign economics
* Customer behavior
* Booking growth
* Attribution
* Measurement anomalies

The underlying data-generation assumptions, customer journey design, attribution rules, and data-model decisions are documented in `DATA_DESIGN.md`.

---

# Conclusion

The analysis shows that **marketing performance should not be evaluated through a single acquisition metric**.

Brand Search and Hotel Deals demonstrate the strongest current acquisition economics, while customer behavior reveals an increasingly important contribution from repeat bookings.

At the same time, CMP008 demonstrates why reported attribution requires scrutiny before being translated directly into investment decisions.

The resulting decision framework is:

> **Scale demonstrated economics. Optimize weaker economics. Validate promising signals. Investigate measurement anomalies.**

The broader objective is to connect **data requirements, analytical modeling, marketing measurement, and business decision-making** into one consistent workflow.
