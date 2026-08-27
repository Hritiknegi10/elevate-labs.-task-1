# elevate-labs.-task-1

#Task 1 

Data Cleaning and Preprocessing

#Objective

*Clean and prepare a raw retail sales dataset containing missing values, duplicate records, inconsistent text formats, mixed date formats, and invalid numeric values.

#Tool Used

Python (Pandas)

#Dataset

1.File: raw_sales_data.csv

2.Dataset type: Retail Sales Data

3.Raw rows: 126

4.Raw columns: 12

5.The raw file intentionally contains common real-world data-quality issues so the full cleaning workflow can be demonstrated.

#Data Cleaning Performed

1.Standardized column names to lowercase.

2.Removed 6 exact duplicate rows.

3.Trimmed extra spaces from text fields.

4.Standardized inconsistent values in product, category, region, and payment method columns.

5.Converted mixed date formats to ISO format YYYY-MM-DD.

6.Removed 2 rows with missing/invalid dates.

7.Filled missing customer names with Unknown Customer.

8.Filled missing regions with the most frequent valid region.

9.Filled missing category/product values with Unknown labels.

10.Converted quantity, unit price, discount, and cost columns to numeric data types.

11.Replaced invalid/non-positive quantities with the median valid quantity.

12.Replaced invalid/non-positive unit prices with the median valid unit price.

13.Filled missing cost values using 70% of cleaned unit price.

14.Standardized discount values to decimal form and limited them to the valid 0–50% range.

15.Recalculated sales from cleaned quantity, unit price, and discount.

16.Added a derived profit column.

17.Performed final checks for duplicates, missing values, data types, and logical validity.

#Result

1.Final cleaned rows: 118

2.Final columns: 13

3.Duplicate rows remaining: 0

4.Invalid dates remaining: 0

5.Critical missing values remaining: 0

6.Output file: cleaned_sales_data.csv
