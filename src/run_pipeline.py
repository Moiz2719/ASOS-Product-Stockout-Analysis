"""Run the full ASOS product stockout analysis pipeline in order."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "clean_data.py",
    "extract_brands.py",
    "analyze_stockouts.py",
    "create_visualizations.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = ROOT / "src" / script
        print(f"\n=== Running {script} ===", flush=True)
        subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)
    print("\nPipeline completed. Review outputs/ and check brand labels before interpreting results.")


if __name__ == "__main__":
    main()
