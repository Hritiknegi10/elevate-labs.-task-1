import pandas as pd
import numpy as np

INPUT_FILE = "raw_sales_data.csv"
OUTPUT_FILE = "cleaned_sales_data.csv"

# Load
df = pd.read_csv(INPUT_FILE)
print("Raw shape:", df.shape)

# 1. Clean column names
df.columns = (
    df.columns.str.strip()
      .str.lower()
      .str.replace("%", "pct", regex=False)
      .str.replace("/", "_", regex=False)
      .str.replace(r"[^a-z0-9]+", "_", regex=True)
      .str.replace(r"_+", "_", regex=True)
      .str.strip("_")
)

# 2. Remove exact duplicates
df = df.drop_duplicates().copy()

# 3. Trim text values
text_cols = ["customer_name", "product", "category", "region", "payment_method"]
for col in text_cols:
    df[col] = df[col].astype("string").str.strip()

# 4. Parse dates (raw file intentionally has multiple formats)
def parse_mixed_date(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NaT
    value = str(value).strip()
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%b %d, %Y", "%d-%m-%Y"]
    for fmt in formats:
        parsed = pd.to_datetime(value, format=fmt, errors="coerce")
        if not pd.isna(parsed):
            return parsed
    return pd.NaT

df["order_date"] = df["order_date"].apply(parse_mixed_date)
df = df.dropna(subset=["order_date"]).copy()

# 5. Standardize / fill text
df["customer_name"] = df["customer_name"].fillna("").replace("", "Unknown Customer").str.title()
df["product"] = df["product"].fillna("").replace("", "Unknown Product").str.title()
df["product"] = df["product"].replace({
    "Usb-C Hub": "USB-C Hub",
    "Led Desk Lamp": "LED Desk Lamp"
})

df["category"] = df["category"].fillna("").replace("", "Unknown").str.title()
df["category"] = df["category"].replace({
    "Home & Office": "Home & Office",
    "Office Supplies": "Office Supplies"
})

df["region"] = df["region"].str.title()
valid_regions = ["North", "South", "East", "West"]
region_mode = df.loc[df["region"].isin(valid_regions), "region"].mode()[0]
df.loc[~df["region"].isin(valid_regions), "region"] = region_mode
df["region"] = df["region"].fillna(region_mode)

df["payment_method"] = df["payment_method"].str.upper().replace({
    "CARD": "Card",
    "CASH": "Cash",
    "UPI": "UPI"
}).fillna("Unknown")

# 6. Convert numeric columns
def clean_numeric(series):
    return pd.to_numeric(
        series.astype("string")
              .str.replace("₹", "", regex=False)
              .str.replace("$", "", regex=False)
              .str.replace(",", "", regex=False)
              .str.strip(),
        errors="coerce"
    )

df["quantity"] = clean_numeric(df["quantity"])
df["unit_price"] = clean_numeric(df["unit_price"])
df["cost_unit"] = clean_numeric(df["cost_unit"])

def clean_discount(value):
    if pd.isna(value) or str(value).strip() == "":
        return 0.0
    s = str(value).strip()
    if s.endswith("%"):
        return pd.to_numeric(s[:-1], errors="coerce") / 100
    n = pd.to_numeric(s, errors="coerce")
    if pd.isna(n):
        return 0.0
    return n / 100 if n > 1 else n

df["discount_pct"] = df["discount_pct"].apply(clean_discount).clip(0, 0.50)

# 7. Fix invalid numeric values
qty_median = df.loc[df["quantity"] > 0, "quantity"].median()
df.loc[df["quantity"].isna() | (df["quantity"] <= 0), "quantity"] = qty_median
df["quantity"] = df["quantity"].round().astype(int)

price_median = df.loc[df["unit_price"] > 0, "unit_price"].median()
df.loc[df["unit_price"].isna() | (df["unit_price"] <= 0), "unit_price"] = price_median

df.loc[df["cost_unit"].isna() | (df["cost_unit"] <= 0), "cost_unit"] = (
    df["unit_price"] * 0.70
)

# 8. Recalculate reliable business fields
df["sales"] = (
    df["quantity"] * df["unit_price"] * (1 - df["discount_pct"])
).round(2)

df["profit"] = (
    df["quantity"] *
    ((df["unit_price"] * (1 - df["discount_pct"])) - df["cost_unit"])
).round(2)

# 9. Rename and format
df = df.rename(columns={"cost_unit": "cost_per_unit"})
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")

final_cols = [
    "order_id", "order_date", "customer_name", "product", "category", "region",
    "quantity", "unit_price", "discount_pct", "cost_per_unit",
    "payment_method", "sales", "profit"
]
df = df[final_cols]

# 10. Final data-quality checks
print("Final shape:", df.shape)
print("Duplicates:", df.duplicated().sum())
print("Missing values:")
print(df.isna().sum())
print("Data types:")
print(df.dtypes)

assert df.duplicated().sum() == 0
assert df.isna().sum().sum() == 0
assert (df["quantity"] > 0).all()
assert (df["unit_price"] > 0).all()
assert df["discount_pct"].between(0, 0.50).all()

df.to_csv(OUTPUT_FILE, index=False)
print(f"Cleaned data saved to: {OUTPUT_FILE}")
