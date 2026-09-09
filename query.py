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
        # Force a massive width so no columns or text are hidden by '...'
        result.show(max_width=10000)
    finally:
        con.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python query.py <query_file>")
        sys.exit(1)

    run_query(sys.argv[1])