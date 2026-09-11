# Marketing Performance Data Platform

## Overview

The objective of this analysis is to evaluate the effectiveness of marketing acquisition across the customer journey — from initial campaign exposure and customer acquisition to customer value, repeat bookings, and attribution reliability.

The analysis combines marketing performance, customer behavior, booking activity, and campaign attribution to answer a broader business question:

> **Which marketing activities are generating valuable customers efficiently, how is customer behavior contributing to growth, and how much confidence should be placed in reported campaign performance?**
> 

The analysis covers:

**Marketing Touchpoints → Customer Acquisition → Campaign Economics → Customer Quality → Booking Growth → Attribution Integrity → Business Recommendations**

---

## Business Questions

The analysis focuses on seven questions:

1. How are customers being acquired across paid and non-paid sources?
2. Which campaigns acquire customers most efficiently?
3. Do different acquisition campaigns produce meaningfully different customer behavior?
4. Which campaigns are associated with higher observed customer value?
5. How is the contribution of new versus repeat bookings changing over time?
6. Can attributed bookings be interpreted as incremental business impact?
7. Where should marketing investment be continued, optimized, validated, or investigated?

---

# Key Findings

## Paid marketing is the primary acquisition engine

In 2025, **5,456 customers** made at least one booking.

| Acquisition Source | Customers | Share |
| --- | --- | --- |
| Paid Campaign | 4,638 | **85.01%** |
| Organic / Direct / Unattributed | 818 | 14.99% |
| **Total** | **5,456** | **100%** |

Paid marketing therefore represents the primary customer acquisition engine.

The non-paid / unattributed group should not be interpreted as purely organic acquisition. It represents customers whose first booking did not receive attribution from an eligible non-direct marketing campaign under the defined attribution rules.

---

## Brand Search and Hotel Deals show the strongest acquisition economics

Among the normal campaigns:

| Campaign | Acquired | Acquisition Share | CAC | ROAS | Avg. First Booking |
| --- | --- | --- | --- | --- | --- |
| Brand Search | 1,146 | 24.71% | **73.12** | **4.85** | 354.52 |
| Hotel Deals | 931 | 20.07% | **79.31** | **4.84** | **383.86** |
| Generic Search | 1,137 | 24.52% | 100.51 | 3.65 | 366.91 |
| Summer Sale | 946 | 20.39% | 101.17 | 3.67 | 370.94 |
| Travel Inspiration | 458 | 9.87% | 95.84 | 3.81 | 365.19 |

**Brand Search** combines the largest acquisition volume with the cheapest CAC and highest first-booking ROAS.

**Hotel Deals** shows similarly strong acquisition efficiency and the highest average first-booking value among the normal campaigns.

This makes both campaigns the strongest current investment candidates, subject to validating marginal economics as spend increases.

---

## Acquisition efficiency differentiates campaigns more than conversion rate

Campaign conversion rates are relatively close across the major campaigns:

| Campaign | Reached | Converted | Conversion |
| --- | --- | --- | --- |
| Brand Search | 4,449 | 3,186 | 71.61% |
| Generic Search | 4,355 | 3,178 | 72.97% |
| Summer Sale | 3,930 | 2,874 | 73.13% |
| Hotel Deals | 3,952 | 2,868 | 72.57% |
| Travel Inspiration | 2,276 | 1,730 | 76.01% |

This suggests that observed conversion rate is not a major differentiator among the normal campaigns.

The more meaningful differences are in **acquisition cost, scale, and downstream customer value**.

ROAS should also be interpreted carefully: it is calculated using first-booking value and therefore **does not represent profit or full customer lifetime value.**

---

## Customer behavior is broadly similar across campaigns

Customers are segmented by observed booking frequency:

- **One-time:** 1 booking
- **Repeat:** 2 bookings
- **Frequent:** 3+ bookings

Across the major campaigns:

| Campaign | One-time | Repeat | Frequent |
| --- | --- | --- | --- |
| Brand Search | 61.7% | 16.7% | 21.6% |
| Generic Search | 62.4% | 16.5% | 21.2% |
| Summer Sale | 64.3% | 14.6% | 21.1% |
| Hotel Deals | 63.8% | 14.9% | 21.3% |
| Travel Inspiration | 64.6% | 15.9% | 19.4% |

The customer mix is relatively consistent, with no strong evidence that the major campaigns acquire fundamentally different customers based on booking frequency.

Observed monetary value provides more differentiation.

### Observed value among repeat customers

| Campaign | Avg. Customer Value |
| --- | --- |
| Hotel Deals | **791** |
| Generic Search | 748 |
| Brand Search | 722 |
| Travel Inspiration | 708 |
| Summer Sale | 664 |

### Observed value among frequent customers

| Campaign | Avg. Customer Value |
| --- | --- |
| Travel Inspiration | **1,327** |
| Brand Search | 1,319 |
| Generic Search | 1,265 |
| Summer Sale | 1,238 |
| Hotel Deals | 1,233 |

This shows why customer quality should not be evaluated using booking frequency alone.

Travel Inspiration, for example, has the lowest frequent-customer share among the major campaigns but the highest observed value among frequent customers.

Observed customer value is not full LTV. Customers acquired earlier in the year have a longer opportunity to generate additional bookings, so these values should be interpreted directionally.

---

# Growth Context

The customer base generated:

- **8,456 customers reached**
- **5,456 customers who booked**
- **9,140 total bookings**
- **1.68 bookings per converted customer**

The composition of monthly bookings changed substantially during the year.

| Month | New Bookings | Repeat Bookings | Total | Repeat Share |
| --- | --- | --- | --- | --- |
| Jan | 98 | 2 | 100 | 2.00% |
| Mar | 531 | 137 | 668 | 20.51% |
| Jun | 490 | 345 | 835 | 41.32% |
| Sep | 506 | 433 | 939 | 46.11% |
| Oct | 469 | 431 | 900 | 47.89% |
| Dec | 521 | 424 | 945 | 44.87% |

Repeat bookings increased from **2.00% of January bookings to roughly 45–48% during much of the second half of the year**.

This does not establish that retention improved, since the existing customer base naturally accumulates over time.

It does establish that **existing customers became an increasingly important contributor to booking volume**.

The growth opportunity should therefore not be framed purely as customer acquisition. Rebooking and customer value are important components of the growth strategy.

---

# Attribution Integrity

## Attribution methodology

Campaign attribution uses a:

- **Last-touch** model
- **Non-direct** marketing touchpoints
- **30-day lookback window**

For each booking, the most recent eligible marketing touchpoint within the preceding 30 days receives attribution credit.

The model answers:

> **Which eligible marketing touchpoint receives reporting credit?**
> 

It does not answer:

> **Would the booking have happened without the campaign?**
> 

Therefore:

> **Attributed booking ≠ proven incremental booking.**
> 

This distinction is critical when using campaign performance to make investment decisions.

---

## CMP008 investigation

CMP008 — Weekend Getaway — presents an unusual attribution pattern.

| Metric | Observation |
| --- | --- |
| Customers reached | 132 |
| Customers subsequently booking | 118 |
| Observed conversion | **89.39%** |
| Attributed bookings | 38 |
| Attributed bookings with prior marketing exposure | 36 |
| Prior marketing exposure rate | **94.74%** |

The combination of unusually high observed conversion, limited reach, short campaign duration, and high prior marketing exposure makes CMP008 an attribution-quality signal worth investigating.

However, the available data does **not** establish that CMP008:

- stole attribution from another campaign
- caused the bookings
- generated no incremental demand

In conclusion:

> **CMP008 should not be benchmarked against the normal campaigns until its attribution behavior is better understood.**
> 

---

# Business Recommendations

## Campaign investment

| Campaign | Recommended Action | Rationale |
| --- | --- | --- |
| **Brand Search** | Continue / consider scaling | Strongest combination of scale, CAC, ROAS, and observed customer value |
| **Hotel Deals** | Continue / investment candidate | Strong CAC and ROAS with high first-booking and repeat-customer value |
| **Generic Search** | Optimize before scaling | Meaningful scale but materially weaker CAC and ROAS |
| **Summer Sale** | Review and optimize | Meaningful scale but weaker acquisition economics and lower repeat-customer value |
| **Travel Inspiration** | Validate before scaling | Interesting frequent-customer value signal despite weaker acquisition efficiency |
| **CMP008** | Investigate separately | Unusual attribution pattern and insufficient evidence for normal benchmarking |

The appropriate scaling principle is:

> **Scale demonstrated economics, optimize weaker economics, validate promising signals, and investigate measurement anomalies before increasing investment.**
> 

Scaling decisions should also consider marginal CAC and incrementality rather than assuming historical performance will remain constant.

---

## Broader growth priorities

### 1. Acquire efficiently

Paid campaigns account for 85.01% of acquired customers, making acquisition efficiency strategically important.

Investment should prioritize campaigns that demonstrate strong economics at sufficient scale.

### 2. Increase value from existing customers

Repeat bookings became an increasingly important contributor to booking volume.

Relevant areas for further optimization include:

- customer lifecycle segmentation
- rebooking campaigns
- personalized offers
- post-booking engagement
- cohort-based customer value measurement

### 3. Improve measurement confidence

Campaign reporting should distinguish between:

**Observed attribution**

and

**Incremental business impact**

Attribution remains useful for performance reporting, but investment decisions should incorporate measurement confidence.

---

# Analytical Limitations

### Supported by the analysis

The data supports conclusions about:

- campaign acquisition volume
- acquisition share
- CAC
- first-booking ROAS
- customer booking-frequency segments
- observed customer booking value
- booking growth composition
- attribution assignments under the defined model
- unusual attribution patterns

### Not established by the analysis

The analysis does not establish:

- true campaign profitability
- incremental revenue
- causal campaign impact
- complete customer lifetime value
- causal differences in retention between campaigns
- whether CMP008 displaced or stole attribution
- whether CMP008 generated incremental demand

These limitations define the appropriate confidence level for each business decision.

---

# Data & Technical Architecture

The analytical environment consists of:

- **Python** — data generation, ingestion, and pipeline execution
- **SQL** — analytical transformations and business logic
- **DuckDB** — local analytical database
- **Git / GitHub** — version control

### Core tables

- `customers`
- `touchpoints`
- `bookings`
- `campaigns`
- `channels`
- `ad_performance`
- `customer_first_booking`
- `acquired_customer_behavior`

### Pipeline

```
Data Generation
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
Funnel & Growth
      ↓
Attribution Integrity
      ↓
Business Recommendations
```

The analytical layer is separated from the data-generation and ingestion processes so that the underlying data can be regenerated while analytical logic remains reusable.

---

# Synthetic Data & Analytical Environment

All data used in the analysis is synthetic.

The dataset was generated to simulate a realistic OTA marketing environment while preserving relationships between customer journeys, marketing touchpoints, bookings, and campaign attribution.

The synthetic environment contains:

- **40,890 marketing touchpoints**
- **8,456 customers reached**
- **5,456 customers with bookings**
- **9,140 bookings**
- booking activity spanning **January–December 2025**

The data includes intentionally constructed scenarios such as:

- repeat customer journeys
- cross-campaign marketing exposure
- Direct / Organic interactions
- 30-day attribution lookback behavior
- different campaign performance profiles
- non-converting touchpoints
- attribution-quality anomalies

The purpose of the synthetic environment is to support analysis of realistic business questions and edge cases without exposing real customer or company data.

For the underlying data-generation logic, attribution assumptions, customer journey design, and data-model decisions, see `DATA_DESIGN.md`.