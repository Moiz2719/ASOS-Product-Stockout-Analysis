"""Create brand-level and product-level summaries for stockout analysis."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "processed" / "products_enriched.csv"
OUTPUT_DIR = ROOT / "outputs"


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Run src/extract_brands.py first; products_enriched.csv was not found.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_FILE)

    brand_summary = (
        df.groupby("Brand", dropna=False)
        .agg(
            Product_Listings=("Brand", "size"),
            Products_With_Stockouts=("Stockout_Count", lambda s: int((s > 0).sum())),
            Total_Stockout_Size_Entries=("Stockout_Count", "sum"),
            Average_Stockout_Rate=("Stockout_Rate", "mean"),
            Estimated_Lost_Revenue=("Lost_Revenue", "sum"),
        )
        .reset_index()
        .sort_values("Product_Listings", ascending=False)
    )
    brand_summary.to_csv(OUTPUT_DIR / "brand_summary.csv", index=False)

    top_products = df.sort_values("Lost_Revenue", ascending=False).head(20)
    columns = [c for c in ["Brand", "name", "price", "Stockout_Count", "Stockout_Rate", "Lost_Revenue", "url"] if c in top_products]
    top_products[columns].to_csv(OUTPUT_DIR / "top_products_by_estimated_lost_revenue.csv", index=False)

    stockout_overview = pd.DataFrame([{
        "Product_Listings": int(len(df)),
        "Products_With_Stockouts": int((df["Stockout_Count"] > 0).sum()),
        "Total_Stockout_Size_Entries": int(df["Stockout_Count"].sum()),
        "Mean_Stockout_Rate": float(df["Stockout_Rate"].mean()) if len(df) else 0.0,
        "Total_Estimated_Lost_Revenue": float(df["Lost_Revenue"].sum()),
        "Exact_Duplicate_Rows_Retained": int(df.duplicated().sum()),
    }])
    stockout_overview.to_csv(OUTPUT_DIR / "stockout_overview.csv", index=False)

    print(f"Saved: {OUTPUT_DIR / 'brand_summary.csv'}")
    print(f"Saved: {OUTPUT_DIR / 'top_products_by_estimated_lost_revenue.csv'}")
    print(f"Saved: {OUTPUT_DIR / 'stockout_overview.csv'}")
    print("Reminder: price × stockout count is a proxy, not observed sales loss.")


if __name__ == "__main__":
    main()
