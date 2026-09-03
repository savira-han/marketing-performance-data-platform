## Synthetic Data Design

This project uses synthetic data designed to simulate a realistic OTA (Online Travel Agency) marketing analytics environment.

The dataset is intentionally more complex than a collection of independently generated CSV files. Instead, customer journeys are generated first, and related marketing touchpoints, bookings, and attribution are derived from those journeys.

### Why the data is intentionally complex

The additional complexity is driven by the business questions this project is designed to answer.

A simple synthetic dataset could demonstrate SQL queries and basic aggregation, but it would not provide enough realistic relationships to investigate questions such as:

* Which campaigns acquire customers who generate repeat bookings?
* Can a customer be acquired through one campaign and later re-engaged by another?
* How much booking volume is actually attributable to marketing?
* Which campaigns generate efficient acquisition versus high-quality customers?
* Does strong campaign-reported performance represent incremental business impact?
* How do acquisition, customer value, marketing spend, and profitability connect?

To support these questions, the data generator models customer journeys before generating the individual records used by the analytical pipeline.

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
Marketing performance & profitability
```

The synthetic data includes intentional scenarios such as repeat bookings, cross-campaign customer journeys, Direct/Organic bookings, attribution lookback windows, campaign seasonality, different campaign performance profiles, and non-converting marketing touchpoints.

One campaign also contains an intentional attribution-quality challenge. The campaign appears highly effective in its raw performance and attribution metrics, but its exposure behavior is designed to test whether attributed conversions represent genuine incremental performance or simply capture credit that would otherwise belong to Direct/Organic activity.

The purpose of these scenarios is not to reproduce a real company's data exactly. Instead, the dataset is designed to reproduce the types of relationships, edge cases, and analytical problems that can occur in a real marketing analytics environment.

For the detailed data model, customer journey logic, attribution rules, and synthetic-data design decisions, see [`DATA_DESIGN.md`](DATA_DESIGN.md).
