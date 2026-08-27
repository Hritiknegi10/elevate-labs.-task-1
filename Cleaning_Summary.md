# Cleaning Summary — Task 1

## Dataset
Retail Sales Data

## Before Cleaning
- Rows: **126**
- Columns: **12**
- Exact duplicate rows: **6**
- Missing customer names: **4**
- Missing regions: **5**
- Missing categories: **3**
- Missing products: **2**
- Invalid/non-positive/missing quantity values: **4**
- Invalid/non-positive/missing unit price values: **3**
- Invalid or missing dates in unique records: **2**
- Text and date formats were inconsistent.

## Cleaning Actions
- Renamed columns into clean lowercase `snake_case`.
- Removed duplicate records.
- Trimmed spaces and standardized text capitalization.
- Standardized region and payment method values.
- Converted all valid dates to `YYYY-MM-DD`.
- Removed rows with invalid/missing dates.
- Filled text missing values with appropriate labels/mode.
- Converted numeric columns and fixed invalid quantities/prices.
- Standardized discounts into decimal values.
- Filled missing costs using a transparent business rule.
- Recalculated sales and calculated profit from cleaned inputs.
- Checked the final dataset for duplicates, missing critical values, and invalid numeric values.

## After Cleaning
- Rows: **118**
- Columns: **13**
- Duplicates remaining: **0**
- Invalid dates remaining: **0**
- Critical missing values remaining: **0**
- Dataset is ready for analysis, visualization, or modeling.
