from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent


def run_step(script_name):
    script_path = PROJECT_ROOT / "src" / script_name

    print(f"\n{'=' * 60}")
    print(f"Running: {script_name}")
    print(f"{'=' * 60}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline failed while running {script_name}"
        )


def main():
    print("Starting marketing data pipeline...")

    run_step("generate_data.py")
    run_step("ingest_data.py")

    print(f"\n{'=' * 60}")
    print("Pipeline completed successfully")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()