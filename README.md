# Marketing Performance Data Platform

An end-to-end marketing analytics project that combines **data engineering, SQL analysis, customer behavior analysis, and business decision-making** in an Online Travel Agency (OTA) context.

The project is designed around a practical marketing question:

> **How can a marketing team understand not only which campaigns acquire customers, but also how efficiently they acquire them, what those customers do afterward, and whether the reported performance can be trusted?**

The analysis covers the full journey:

**Marketing touchpoints → Customer acquisition → Campaign efficiency → Customer quality → Booking growth → Attribution integrity → Business recommendations**

---

## Business Context

Marketing teams often evaluate campaigns using metrics such as spend, CAC, conversion rate, and ROAS.

Those metrics are useful, but they do not tell the whole story.

A campaign can have:

* strong acquisition volume but poor efficiency
* efficient acquisition but weak downstream customer value
* high reported conversion but limited evidence of incremental impact
* attractive attribution metrics that do not necessarily represent additional business

This project therefore looks beyond campaign-level KPIs and connects **acquisition economics, customer behavior, growth, and measurement confidence**.

---

## Key Business Questions

The analysis is designed to answer:

1. **How are customers being acquired?**
2. **Which campaigns acquire customers efficiently?**
3. **Do different campaigns produce meaningfully different customer behavior?**
4. **How does customer value differ across acquisition sources and customer segments?**
5. **How does the contribution of new vs. repeat bookings change over time?**
6. **Can campaign-attributed bookings be interpreted as incremental business impact?**
7. **Where should marketing investment be maintained, optimized, investigated, or validated?**

---

# Key Findings

## 1. Paid marketing is the primary acquisition engine

In 2025, **5,456 customers** made at least one booking.

Of these:

* **4,638 customers (85.01%)** were acquired through paid campaigns
* **818 customers (14.99%)** were classified as Organic / Direct / Unattributed

This makes paid marketing the dominant customer acquisition engine in the dataset.

However, an unattributed first booking does not necessarily mean the customer was organically acquired. It means there was no attributable non-direct marketing campaign under the defined attribution rules.

---

## 2. Brand Search and Hotel Deals show the strongest acquisition economics

Among the normal campaigns:

| Campaign           | Acquired |       CAC |     ROAS | Avg. First Booking |
| ------------------ | -------: | --------: | -------: | -----------------: |
| Brand Search       |    1,146 | **73.12** | **4.85** |             354.52 |
| Hotel Deals        |      931 | **79.31** | **4.84** |         **383.86** |
| Generic Search     |    1,137 |    100.51 |     3.65 |             366.91 |
| Summer Sale        |      946 |    101.17 |     3.67 |             370.94 |
| Travel Inspiration |      458 |     95.84 |     3.81 |             365.19 |

Brand Search combines the largest acquisition volume with the lowest CAC and highest first-booking ROAS.

Hotel Deals shows similarly strong acquisition efficiency while producing the highest average first-booking value among the normal campaigns.

This makes **Brand Search and Hotel Deals the strongest current investment candidates**.

---

## 3. Customer behavior is more similar across campaigns than acquisition efficiency

Major campaigns have broadly similar customer mixes:

| Campaign           | One-time | Repeat | Frequent |
| ------------------ | -------: | -----: | -------: |
| Brand Search       |    61.7% |  16.7% |    21.6% |
| Generic Search     |    62.4% |  16.5% |    21.2% |
| Summer Sale        |    64.3% |  14.6% |    21.1% |
| Hotel Deals        |    63.8% |  14.9% |    21.3% |
| Travel Inspiration |    64.6% |  15.9% |    19.4% |

There is no strong evidence that the major campaigns acquire fundamentally different customer populations based on booking frequency alone.

Observed monetary value provides more differentiation.

For example:

* Hotel Deals had the highest observed value among repeat customers: **791**
* Travel Inspiration had the highest observed value among frequent customers: **1,327**
* Brand Search remained strong across both acquisition economics and downstream customer value

This suggests that **customer quality should not be evaluated using retention or booking frequency alone**.

> Observed customer value is not full LTV. Customers acquired earlier in the year have more opportunity to generate additional bookings.

---

## 4. Existing customers became increasingly important to booking growth

The dataset contains:

* **8,456 customers reached**
* **5,456 customers who booked**
* **9,140 total bookings**
* **1.68 bookings per converted customer**

The composition of monthly bookings also changed during the year.

Repeat bookings represented:

* **2.00%** of January bookings
* **20.51%** in March
* **41.32%** in June
* **46.11%** in September
* **47.89%** in October
* **44.87%** in December

This does not prove that retention improved, because the existing customer base naturally accumulates over time.

It does show that **existing customers became an increasingly important contributor to booking volume**.

Therefore, growth should not be viewed purely as an acquisition problem. Rebooking and customer value are also important parts of the growth strategy.

---

## 5. Attribution credit is not the same as incremental impact

The project uses a:

* last-touch attribution model
* non-direct marketing touchpoints
* 30-day lookback window

This answers:

> **Which eligible marketing touchpoint receives reporting credit?**

It does not answer:

> **Would the booking have happened without that campaign?**

This distinction becomes important when evaluating campaign economics.

### CMP008 attribution investigation

CMP008 — Weekend Getaway — was intentionally designed as an attribution-quality challenge in the synthetic dataset.

It had:

* 132 customers reached
* 118 customers who subsequently booked
* **89.39% observed conversion**
* 38 attributed bookings
* 36 of 38 attributed bookings (**94.74%**) had prior marketing exposure

The pattern is unusual enough to investigate, but the analysis does **not** establish that CMP008:

* stole attribution from another campaign
* caused the bookings
* generated no incremental demand

The appropriate conclusion is:

> **CMP008 is an attribution-quality signal that should reduce confidence in using its observed performance as a normal campaign benchmark.**

A stronger causal design, such as a holdout or geo experiment, would be required to establish incrementality.

---

# Business Recommendations

The analysis leads to a focused set of actions.

### Continue / consider scaling

**Brand Search**

Strongest combination of scale and efficiency:

* 1,146 acquired customers
* CAC: 73.12
* ROAS: 4.85

Scale should still be evaluated using marginal CAC rather than assuming historical efficiency will remain constant.

**Hotel Deals**

Strong acquisition efficiency and high observed customer value:

* CAC: 79.31
* ROAS: 4.84
* highest normal-campaign first-booking value
* highest observed repeat-customer value

---

### Optimize before scaling

**Generic Search**

Meaningful acquisition scale, but CAC is materially higher than Brand Search and Hotel Deals.

**Summer Sale**

Similar scale to Generic Search, with weaker acquisition economics and the lowest observed repeat-customer value among the major campaigns.

Both should be optimized before additional budget is committed.

---

### Validate before scaling

**Travel Inspiration**

Acquisition economics are weaker, but frequent customers show the highest observed value among the major campaigns.

This is an interesting signal that warrants further cohort/LTV analysis rather than immediate scaling.

---

### Investigate separately

**Weekend Getaway (CMP008)**

The campaign's unusual conversion and attribution pattern make it unsuitable for normal campaign benchmarking.

It should be treated as a measurement investigation rather than as a high-performing campaign.

---

# Analytical Framework

Campaign performance is evaluated across five dimensions:

**Scale**
→ How many customers does the campaign acquire?

**Efficiency**
→ How much does it cost to acquire them?

**Initial Value**
→ What is the value of the first booking?

**Customer Quality**
→ What happens after acquisition?

**Measurement Confidence**
→ How reliable is the performance signal?

This prevents the analysis from reducing campaign performance to a single KPI such as ROAS.

---

# Attribution Approach

The project uses a **last-touch, non-direct, 30-day lookback attribution model**.

For each booking:

1. Identify marketing touchpoints before the booking.
2. Restrict eligible touchpoints to the previous 30 days.
3. Exclude Direct / Organic touchpoints.
4. Assign credit to the most recent eligible marketing touchpoint.

The customer's **acquisition campaign** is determined separately from later booking attribution.

This distinction allows the project to answer both:

* Which campaign acquired the customer?
* Which campaign received attribution for later bookings?

A customer may therefore be acquired through one campaign and later have bookings attributed to another campaign.

---

# Customer Quality Framework

Customers are segmented based on observed booking frequency:

| Segment  | Definition  |
| -------- | ----------- |
| One-time | 1 booking   |
| Repeat   | 2 bookings  |
| Frequent | 3+ bookings |

Across the 5,456 acquired customers:

* **3,443 (63.1%)** were One-time
* **847 (15.5%)** were Repeat
* **1,166 (21.4%)** were Frequent

Customer value is based on observed booking value across the available 2025 observation window.

It should not be interpreted as complete lifetime value.

---

# Data & Technical Architecture

The project uses synthetic data designed to simulate a realistic OTA marketing analytics environment.

Customer journeys are generated first, with related marketing touchpoints, bookings, and attribution derived from those journeys.

### Core tables

* `customers`
* `touchpoints`
* `bookings`
* `campaigns`
* `channels`
* `ad_performance`
* `customer_first_booking`
* `acquired_customer_behavior`

### Technology

* **Python** — data generation, ingestion, pipeline execution
* **SQL** — analytical transformations and business logic
* **DuckDB** — local analytical database
* **Git / GitHub** — version control and project documentation

The project is designed to run locally without requiring a cloud data warehouse.

---

# Project Pipeline

```text
Synthetic Data Generation
        ↓
Python Ingestion
        ↓
DuckDB
        ↓
SQL Transformations
        ↓
Customer Acquisition
        ↓
CAC & ROAS
        ↓
Customer Quality
        ↓
Funnel & Growth Analysis
        ↓
Attribution Integrity
        ↓
Business Recommendations
```

The pipeline is designed so that data generation and ingestion can be rerun consistently, while analytical queries remain separate from the underlying data-generation process.

---

# Synthetic Data Design

The dataset is intentionally more complex than a collection of independently generated CSV files.

Customer journeys are generated first, and related marketing touchpoints, bookings, and attribution are derived from those journeys.

This allows the dataset to preserve meaningful relationships between:

```text
Customer behavior
       ↓
Marketing touchpoints
       ↓
Bookings
       ↓
Campaign attribution
       ↓
Customer acquisition & quality
       ↓
Marketing performance
       ↓
Business decisions
```

The synthetic data includes intentional scenarios such as:

* repeat bookings
* cross-campaign customer journeys
* Direct / Organic bookings
* attribution lookback windows
* different campaign performance profiles
* non-converting marketing touchpoints
* an attribution-quality challenge involving CMP008

The purpose is not to reproduce a real company's data exactly.

Instead, the dataset is designed to reproduce the types of relationships, edge cases, and analytical questions that can occur in a real marketing analytics environment.

For detailed data-model decisions, customer journey logic, attribution rules, and synthetic-data design, see [`DATA_DESIGN.md`](DATA_DESIGN.md).

---

# Important Limitations

This project uses synthetic data and therefore does not represent actual business performance.

The analysis can demonstrate:

* analytical reasoning
* SQL and data modeling
* data pipeline design
* marketing measurement
* customer behavior analysis
* business recommendation development

However, the analysis cannot establish:

* true campaign profitability
* incremental revenue
* causal campaign impact
* complete customer lifetime value
* whether CMP008 actually caused or displaced bookings

In particular:

> **Attributed revenue should not automatically be interpreted as incremental revenue.**