# Project Overview

## Purpose

Convert the ASOS product-listing notebook into a repeatable analysis workflow. The work focuses on product data quality, brand labels, size availability, and a rough stockout-related revenue proxy.

## Business questions

1. Which brands account for the most product listings?
2. Which products have entries marked `Out of stock`?
3. How does the stockout rate vary across listed products?
4. Which products rank highest under the notebook's `price × Stockout_Count` proxy?

## Input and outputs

- Input: `data/raw/products_asos.csv` (not supplied with the PDF).
- Cleaned table: `data/processed/products_cleaned.csv`.
- Enriched table: `data/processed/products_enriched.csv`.
- Summaries: `outputs/brand_summary.csv`, `outputs/stockout_overview.csv`, and `outputs/top_products_by_estimated_lost_revenue.csv`.
- Charts: `outputs/figures/`.

## Tools

Python, Pandas, Matplotlib, and Seaborn. The supplied notebook does not use a database or SQL, so this project remains a Python/Pandas workflow.
