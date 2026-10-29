"""Generate simple portfolio-ready visualisations from the enriched product data."""
from __future__ import annotations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "processed" / "products_enriched.csv"
OUTPUT_DIR = ROOT / "outputs" / "figures"


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Run src/extract_brands.py first; products_enriched.csv was not found.")
    df = pd.read_csv(INPUT_FILE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    top_brands = df["Brand"].value_counts().head(10).sort_values()
    if not top_brands.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        top_brands.plot(kind="barh", ax=ax)
        ax.set_title("Top 10 Brands by Product Listings")
        ax.set_xlabel("Number of product listings")
        ax.set_ylabel("Brand")
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / "top_brands_by_listings.png", dpi=160)
        plt.close(fig)

    top_revenue = df.nlargest(10, "Lost_Revenue").copy()
    if not top_revenue.empty:
        top_revenue["Product_Label"] = top_revenue.get("name", pd.Series(index=top_revenue.index, dtype=str)).fillna("Unnamed product").astype(str).str.slice(0, 38)
        fig, ax = plt.subplots(figsize=(11, 6))
        top_revenue.sort_values("Lost_Revenue").plot(x="Product_Label", y="Lost_Revenue", kind="barh", legend=False, ax=ax)
        ax.set_title("Top Products by Estimated Lost Revenue")
        ax.set_xlabel("Price × out-of-stock size count (estimate)")
        ax.set_ylabel("Product")
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / "top_products_estimated_lost_revenue.png", dpi=160)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(df["Stockout_Rate"].dropna(), bins=20)
    ax.set_title("Distribution of Product Stockout Rates")
    ax.set_xlabel("Out-of-stock entries / size entries")
    ax.set_ylabel("Number of product listings")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "stockout_rate_distribution.png", dpi=160)
    plt.close(fig)

    print(f"Charts saved to {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
