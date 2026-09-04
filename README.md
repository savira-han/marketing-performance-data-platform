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

## Pipeline

The project uses a local, reproducible pipeline to generate synthetic source data, validate and ingest the raw data, and load it into DuckDB for analysis.

```text
Synthetic data generation
        ↓
Raw CSV data
        ↓
Validation & ingestion
        ↓
DuckDB
        ↓
SQL analysis
```

### Pipeline components

* `src/generate_data.py` — generates the synthetic OTA source data and performs data-generation validations.
* `src/ingest_data.py` — loads the raw CSV files, validates keys, foreign-key relationships, and business-value constraints, then loads the data into DuckDB.
* `analytics.duckdb` — local analytical database containing the ingested source tables.
* `run_pipeline.py` — orchestrates the complete workflow so the project can be executed with a single command.

### Run the pipeline

From the project root:

```bash
python run_pipeline.py
```

The pipeline executes the generation and ingestion steps in the correct order.

The workflow is designed to be safely re-runnable. The DuckDB tables are recreated during ingestion, allowing the database to be rebuilt from the generated source data without relying on a previous database state.

### Current DuckDB tables

The ingestion pipeline creates the following source tables:

| Table            | Description                        |
| ---------------- | ---------------------------------- |
| `customers`      | Customer-level information         |
| `channels`       | Marketing channel definitions      |
| `campaigns`      | Marketing campaign definitions     |
| `touchpoints`    | Customer marketing interactions    |
| `bookings`       | Customer booking transactions      |
| `ad_performance` | Daily campaign performance metrics |

This provides the foundation for the SQL-based marketing and growth analyses developed in the next stage of the project.
