from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "DataCoSupplyChainDataset.csv"
)

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

df = pd.read_csv(
    DATASET_PATH,
    encoding="latin1",
    low_memory=False
)

print("\n========== DATASET OVERVIEW ==========")
print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])

print("\n========== COLUMN NAMES ==========")
for column in df.columns:
    print("-", column)

print("\n========== MISSING VALUES ==========")
print(
    df.isnull()
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

print("\n========== DUPLICATE ROWS ==========")
print("Duplicates:", df.duplicated().sum())

print("\n========== USEFUL GRAPH FIELDS ==========")

possible_fields = [
    "Order Id",
    "Product Name",
    "Category Name",
    "Shipping Mode",
    "Order City",
    "Order Country",
    "Customer City",
    "Customer Country",
    "Delivery Status",
    "Late_delivery_risk"
]

for field in possible_fields:
    if field in df.columns:
        print(f"{field}: {df[field].nunique()} unique values")

print("\nDataset inspection completed!")
# 1. Delivery status distribution
print("\n========== DELIVERY STATUS ==========")
print(df["Delivery Status"].value_counts())

# 2. Late delivery risk
print("\n========== LATE DELIVERY RISK ==========")
print(df["Late_delivery_risk"].value_counts())

# 3. Compare delivery status with risk
print("\n========== STATUS VS RISK ==========")
print(pd.crosstab(
    df["Delivery Status"],
    df["Late_delivery_risk"],
    margins=True
))

# 4. Actual vs scheduled shipping time
print("\n========== SHIPPING DELAY ==========")

df["delay_days"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

print(df["delay_days"].describe())

# 5. Shipping delay by delivery status
print("\n========== DELAY BY STATUS ==========")

print(
    df.groupby("Delivery Status")["delay_days"]
    .agg(["count", "mean", "median", "max"])
)

# 6. Shipping modes
print("\n========== SHIPPING MODE ANALYSIS ==========")

print(pd.crosstab(
    df["Shipping Mode"],
    df["Delivery Status"]
))

# 7. Order processing problems
print("\n========== ORDER STATUS ==========")
print(df["Order Status"].value_counts())

# 8. Shipping mode percentages
print("\n========== SHIPPING MODE PERCENTAGES ==========")

print(
    pd.crosstab(
        df["Shipping Mode"],
        df["Delivery Status"],
        normalize="index"
    ).mul(100).round(2)
)

# 9. Regional delivery risk
print("\n========== REGIONAL DELIVERY RISK ==========")

delivered_df = df[
    df["Delivery Status"] != "Shipping canceled"
].copy()

region_summary = delivered_df.groupby("Order Region").agg(
    total_records=("Order Id", "size"),
    late_records=("Late_delivery_risk", "sum"),
    average_delay_days=("delay_days", "mean")
)

region_summary["late_rate_pct"] = (
    region_summary["late_records"]
    / region_summary["total_records"] * 100
)

print(
    region_summary
    .sort_values("late_rate_pct", ascending=False)
    .round(2)
)

# 10. Market-wise delivery risk
print("\n========== MARKET DELIVERY RISK ==========")

market_summary = delivered_df.groupby("Market").agg(
    total_records=("Order Id", "size"),
    late_records=("Late_delivery_risk", "sum")
)

market_summary["late_rate_pct"] = (
    market_summary["late_records"]
    / market_summary["total_records"] * 100
)

print(
    market_summary
    .sort_values("late_rate_pct", ascending=False)
    .round(2)
)
print("\n========== GRAPH ID VALIDATION ==========")

for column in [
    "Order Id",
    "Order Item Id",
    "Product Card Id",
    "Order Item Cardprod Id"
]:
    print(
        column,
        "| Unique:", df[column].nunique(),
        "| Missing:", df[column].isna().sum()
    )

print("\nProduct ID consistency:")
print(
    (df["Product Card Id"] == df["Order Item Cardprod Id"])
    .value_counts()
)
print("\n========== PRODUCT MAPPING VALIDATION ==========")

print(
    "Maximum product names per product ID:",
    df.groupby("Product Card Id")["Product Name"].nunique().max()
)

print(
    "Maximum categories per product ID:",
    df.groupby("Product Card Id")["Product Category Id"].nunique().max()
)

print("\n========== ORDER ITEM VALIDATION ==========")

print(
    "Maximum orders per order item:",
    df.groupby("Order Item Id")["Order Id"].nunique().max()
)

print(
    "Maximum products per order item:",
    df.groupby("Order Item Id")["Product Card Id"].nunique().max()
)
print("\n========== ORDER LEVEL CONSISTENCY ==========")

order_fields = [
    "Delivery Status",
    "Shipping Mode",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "shipping date (DateOrders)"
]

for column in order_fields:
    max_values = df.groupby("Order Id")[column].nunique().max()

    print(f"{column}: maximum unique values per order = {max_values}")
print("\n========== ADDITIONAL ORDER VALIDATION ==========")

fields = [
    "Order Status",
    "Order Region",
    "Order Country",
    "Market",
    "order date (DateOrders)",
    "Order Customer Id"
]

for column in fields:
    print(
        column,
        ":",
        df.groupby("Order Id")[column].nunique().max()
    )
print("\n========== CUSTOMER VALIDATION ==========")

print(
    "Unique customers:",
    df["Order Customer Id"].nunique()
)

print(
    "Maximum orders per customer:",
    df.groupby("Order Customer Id")["Order Id"].nunique().max()
)

print(
    "Maximum countries per customer:",
    df.groupby("Order Customer Id")["Customer Country"].nunique().max()
)

print(
    "Missing customer IDs:",
    df["Order Customer Id"].isna().sum()
)
print("\n========== CUSTOMER ID CONSISTENCY ==========")

print(
    "Customer ID matches Order Customer ID:",
    (df["Customer Id"] == df["Order Customer Id"]).all()
)

print(
    "Customer segments per customer:",
    df.groupby("Order Customer Id")["Customer Segment"].nunique().max()
)