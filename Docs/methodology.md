# Methodology

## 1. Load and profile

Load `products_asos.csv` with Pandas using `on_bad_lines='skip'`, as shown in the notebook. The PDF reports an initial DataFrame shape of 9,875 rows × 9 columns.

## 2. Clean empty rows and parse prices

Remove rows that are null across all columns. The PDF reports 9,857 rows × 9 columns after this step. Convert `price` from text to a numeric value by extracting the first number, covering examples such as `From 42.50` and `Now 72.00`.

## 3. Inspect duplicates

Count exact duplicate rows and export them for inspection. The PDF reports five duplicate rows. It shows a count and display step, but does not show duplicate removal; the refactored script retains them by default to match that documented workflow.

## 4. Extract brand labels

The notebook reads text after ` by `, then applies a small mapping for shortened labels: `New` → `New Look`, `River` → `River Island`, `Miss` → `Miss Selfridge`, and `TopshopWelcome` → `Topshop`. Some sample labels remain concatenated with product text, such as `StradivariusJacket` and `JDYLow-key`. The refactored script normalises several such visible patterns and uses a product URL fallback if the description does not provide a label. Review the distinct labels before publishing brand insights.

## 5. Calculate stockout measures

Split the `size` string on commas, count entries containing `Out of stock`, and divide that count by the number of non-empty size entries. This reproduces the notebook's approach; its reliability depends on consistent formatting in the `size` field.

## 6. Estimate potential lost revenue

Calculate the `Lost_Revenue` field as `price × Stockout_Count`, following the formula used in the notebook.

## 7. Summarise and visualise

Create brand listing counts, stockout summaries, a ranked product table, and charts for top brands, highest estimated proxy values, and stockout-rate distribution.
