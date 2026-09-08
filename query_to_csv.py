from pathlib import Path
import duckdb
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "analytics.duckdb"
QUERIES_DIR = PROJECT_ROOT / "queries"


def run_query(query_name):
    query_path = QUERIES_DIR / query_name

    if not query_path.exists():
        raise FileNotFoundError(
            f"Query file not found: {query_path}"
        )

    sql = query_path.read_text()

    con = duckdb.connect(str(DB_PATH))
    try:
        result = con.sql(sql)
        
        # 1. Convert DuckDB result to a Pandas DataFrame
        # 2. Output as a clean CSV string (index=False removes row numbers)
        csv_string = result.df().to_csv(index=False)
        
        print(csv_string)
    finally:
        con.close()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python query_to_csv.py <query_file>")
        sys.exit(1)

    run_query(sys.argv[1])
