# Findings and Limitations

## Findings reported in the supplied PDF

- Initial DataFrame shape: **9,875 × 9**.
- Shape after removing fully empty rows: **9,857 × 9**.
- Exact duplicate rows detected: **5**.
- The notebook converts price strings into `float64` by extracting the first number.
- Top five brands by product-listing count reported in the notebook:
  - ASOS: 2,970
  - Topshop: 597
  - River Island: 304
  - Miss Selfridge: 301
  - New Look: 254

The PDF does not include a readable final table for the top five estimated lost-revenue products or a complete stockout summary. Those findings are not invented here.

## Limitations

1. The raw CSV is missing, so the refactored pipeline has not been validated against the original dataset.
2. Brand extraction in the notebook produces concatenated or shortened values for some brands. Normalisation and URL fallback improve handling but still require manual review.
3. Product URLs, listings, and size text may include duplicate listings; the PDF counts five duplicates but does not show a step removing them.
4. `Stockout_Rate` assumes comma-separated values each represent one size availability entry.
5. `Lost_Revenue = price × Stockout_Count` is only a rough proxy. It does not include historical sales, demand, stockout duration, units normally sold per size, discounts, or whether replacement sizes are available.
6. Price extraction uses the first numeric amount. For offers such as `From 42.50` or `Now 72.00`, that value may not be equivalent to a regular, original, or realised transaction price.
7. Product listings may change over time; no scrape timestamp or historical inventory snapshot is evidenced in the PDF.
