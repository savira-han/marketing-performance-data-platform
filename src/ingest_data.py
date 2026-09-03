from pathlib import Path
import duckdb
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "analytics.duckdb"


# Raw tables to ingest
RAW_TABLES = {
    "customers": "customers.csv",
    "channels": "channels.csv",
    "campaigns": "campaigns.csv",
    "touchpoints": "touchpoints.csv",
    "bookings": "bookings.csv",
    "ad_performance": "ad_performance.csv",
}


def load_csv(table_name, filename):
    """Load one raw CSV file into a Pandas DataFrame."""
    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw data file not found for '{table_name}': {file_path}"
        )

    df = pd.read_csv(file_path)

    print(f"✓ Loaded {table_name}: {len(df):,} rows")

    return df


def get_connection():
    """Create a connection to the DuckDB analytics database."""
    return duckdb.connect(str(DB_PATH))


def load_table_to_duckdb(con, table_name, df):
    """Write a Pandas DataFrame into a DuckDB table."""
    con.register("temp_df", df)

    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT * FROM temp_df
    """)

    con.unregister("temp_df")

    print(f"✓ Loaded {table_name} into DuckDB ({len(df):,} rows)")


def validate_table(df, table_name, key_column):
    """Run basic validation checks on an ingested table."""
    if df.empty:
        raise ValueError(f"{table_name} is empty")

    if key_column not in df.columns:
        raise ValueError(
            f"{table_name} is missing expected key column: {key_column}"
        )

    if df[key_column].isna().any():
        raise ValueError(
            f"{table_name} contains null values in {key_column}"
        )

    if df[key_column].duplicated().any():
        raise ValueError(
            f"{table_name} contains duplicate values in {key_column}"
        )

    print(f"✓ {table_name} validation passed")

def validate_composite_key(df, table_name, key_columns):
    """Validate uniqueness and completeness of a composite key."""
    missing_columns = [
        column for column in key_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{table_name} is missing expected columns: {missing_columns}"
        )

    if df[key_columns].isna().any().any():
        raise ValueError(
            f"{table_name} contains null values in its composite key"
        )

    if df.duplicated(subset=key_columns).any():
        raise ValueError(
            f"{table_name} contains duplicate composite keys: {key_columns}"
        )

    print(
        f"✓ {table_name} composite grain validation passed"
    )

def validate_foreign_key(
    child_df,
    child_table,
    child_column,
    parent_df,
    parent_table,
    parent_column
):
    """Validate that all non-null foreign-key values exist in the parent table."""

    child_values = child_df[child_column].dropna()
    parent_values = set(parent_df[parent_column].dropna())

    invalid_values = set(child_values) - parent_values

    if invalid_values:
        raise ValueError(
            f"{child_table}.{child_column} contains "
            f"{len(invalid_values)} invalid values not found in "
            f"{parent_table}.{parent_column}"
        )

    print(
        f"✓ {child_table}.{child_column} → "
        f"{parent_table}.{parent_column} FK validation passed"
    )

def validate_business_values(raw_data):
    """Validate basic business-value constraints."""

    bookings = raw_data["bookings"]
    ad_performance = raw_data["ad_performance"]

    if (bookings["booking_value"] < 0).any():
        raise ValueError("Bookings contain negative booking values")

    if (ad_performance["impressions"] <= 0).any():
        raise ValueError("Ad performance contains non-positive impressions")

    if (ad_performance["clicks"] < 0).any():
        raise ValueError("Ad performance contains negative clicks")

    if (
        ad_performance["clicks"]
        > ad_performance["impressions"]
    ).any():
        raise ValueError("Ad performance contains clicks greater than impressions")

    if (ad_performance["spend"] < 0).any():
        raise ValueError("Ad performance contains negative spend")

    print("✓ Business-value validation passed")




def ingest_data():
    """Run the complete raw-data ingestion pipeline."""

    # Load all raw tables
    raw_data = {}

    for table_name, filename in RAW_TABLES.items():
        raw_data[table_name] = load_csv(table_name, filename)

    # Validate dimension tables
    validate_table(
        raw_data["customers"],
        "customers",
        "customer_id"
    )

    validate_table(
        raw_data["channels"],
        "channels",
        "channel_id"
    )

    validate_table(
        raw_data["campaigns"],
        "campaigns",
        "campaign_id"
    )

    # Validate fact-table grains
    validate_table(
        raw_data["touchpoints"],
        "touchpoints",
        "touchpoint_id"
    )

    validate_table(
        raw_data["bookings"],
        "bookings",
        "booking_id"
    )

    validate_composite_key(
        raw_data["ad_performance"],
        "ad_performance",
        ["campaign_id", "date"]
    )

    # Validate foreign-key relationships
    validate_foreign_key(
        raw_data["bookings"],
        "bookings",
        "customer_id",
        raw_data["customers"],
        "customers",
        "customer_id"
    )

    validate_foreign_key(
        raw_data["bookings"],
        "bookings",
        "attributed_campaign_id",
        raw_data["campaigns"],
        "campaigns",
        "campaign_id"
    )

    validate_foreign_key(
        raw_data["touchpoints"],
        "touchpoints",
        "customer_id",
        raw_data["customers"],
        "customers",
        "customer_id"
    )

    validate_foreign_key(
        raw_data["touchpoints"],
        "touchpoints",
        "campaign_id",
        raw_data["campaigns"],
        "campaigns",
        "campaign_id"
    )

    validate_foreign_key(
        raw_data["ad_performance"],
        "ad_performance",
        "campaign_id",
        raw_data["campaigns"],
        "campaigns",
        "campaign_id"
    )

    validate_foreign_key(
        raw_data["campaigns"],
        "campaigns",
        "channel_id",
        raw_data["channels"],
        "channels",
        "channel_id"
    )

    # Validate business values
    validate_business_values(raw_data)

    # Connect to DuckDB
    con = get_connection()

    print(f"✓ Connected to DuckDB: {DB_PATH}")

    # Load raw data into DuckDB
    for table_name, df in raw_data.items():
        load_table_to_duckdb(con, table_name, df)

    con.close()

    print("✓ DuckDB ingestion completed")

if __name__ == "__main__":
    ingest_data()