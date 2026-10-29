# Data Dictionary

The supplied notebook reports nine source columns. Exact source meanings should be checked against the actual CSV before publication.

| Column | Meaning inferred from notebook | Notes |
|---|---|---|
| `url` | Product page URL | Used as a fallback for readable brand extraction. |
| `name` | Product title | Used in product-level outputs and charts. |
| `size` | Comma-separated size/availability text | Includes size labels and `Out of stock` entries. |
| `category` | Product category | Original field from CSV. |
| `price` | Listed product price | Converted to numeric by extracting the first number from the string. |
| `color` | Product colour | Original field from CSV. |
| `sku` | Product SKU or identifier | Read by Pandas as numeric in the PDF; verify whether it should be treated as an identifier string. |
| `description` | Product description/details text | Source for brand extraction. |
| `images` | Product image metadata/URLs | Original field from CSV; not needed for the current calculations. |

## Derived fields

| Field | Definition |
|---|---|
| `Brand` | Brand label extracted from description text, standardised for known labels shown in the notebook, with URL fallback where available. Unrecognised values require review. |
| `Stockout_Count` | Number of comma-separated size entries containing `Out of stock`. |
| `Stockout_Rate` | `Stockout_Count / number of non-empty comma-separated size entries`. |
| `Lost_Revenue` | `price × Stockout_Count`; an estimate/proxy rather than measured sales loss. |
