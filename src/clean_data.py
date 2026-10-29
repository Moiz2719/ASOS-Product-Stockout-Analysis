"""Load the ASOS CSV, perform the cleaning steps shown in the notebook, and report quality checks."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "raw" / "products_asos.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "products_cleaned.csv"
REPORT_FILE = ROOT / "outputs" / "data_quality_report.json"
DUPLICATES_FILE = ROOT / "outputs" / "duplicate_rows.csv"


def parse_price(value: object) -> float | None:
    """Extract the first numeric amount from values like 'From 42.50' or 'Now 72.00'."""
    if pd.isna(value):
        return None
    match = re.search(r"(\d+\.?\d*)", str(value).replace(",", ""))
    return float(match.group(1)) if match else None


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Source CSV not found: {INPUT_FILE}\n"
            "Download/prepare the authorised file and place it at data/raw/products_asos.csv."
        )

    ROOT.joinpath("data", "processed").mkdir(parents=True, exist_ok=True)
    ROOT.joinpath("outputs").mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_FILE, on_bad_lines="skip")
    original_shape = [int(df.shape[0]), int(df.shape[1])]
    nulls_before = {str(k): int(v) for k, v in df.isna().sum().items()}

    # Mirrors the notebook: discard records that are empty across every column.
    df = df.dropna(how="all").copy()

    # Mirrors the notebook's numeric extraction for prices with prefixes like "Now" or "From".
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"].map(parse_price), errors="coerce")
    else:
        raise KeyError("Expected a 'price' column in products_asos.csv")

    duplicate_count = int(df.duplicated().sum())
    duplicate_rows = df[df.duplicated(keep=False)]
    duplicate_rows.to_csv(DUPLICATES_FILE, index=False)

    # The PDF only counted/displayed duplicates; it did not remove them. Preserve them by default.
    df.to_csv(OUTPUT_FILE, index=False)

    report = {
        "input_file": str(INPUT_FILE.relative_to(ROOT)),
        "original_shape": original_shape,
        "shape_after_dropping_fully_empty_rows": [int(df.shape[0]), int(df.shape[1])],
        "null_counts_before_cleaning": nulls_before,
        "fully_empty_rows_removed": int(original_shape[0] - df.shape[0]),
        "exact_duplicate_rows_detected": duplicate_count,
        "duplicate_rows_exported_to": str(DUPLICATES_FILE.relative_to(ROOT)),
        "duplicates_removed": False,
        "price_dtype_after_conversion": str(df["price"].dtype),
        "cleaned_data_file": str(OUTPUT_FILE.relative_to(ROOT)),
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Original shape: {tuple(original_shape)}")
    print(f"After dropping fully empty rows: {df.shape}")
    print(f"Exact duplicate rows detected (retained, as in the PDF): {duplicate_count}")
    print(f"Saved cleaned data: {OUTPUT_FILE.relative_to(ROOT)}")
    print(f"Saved quality report: {REPORT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
