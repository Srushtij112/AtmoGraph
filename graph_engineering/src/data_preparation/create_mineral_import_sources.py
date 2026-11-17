
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw" / "USGS_MCS_2026"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

FIG2_FILE = RAW_FOLDER / "MCS2026_Fig2_Net_Import_Reliance.csv"
FIG3_FILE = RAW_FOLDER / "MCS2026_Fig3_Major_Import_Sources.csv"

OUTPUT_FILE = OUTPUT_FOLDER / "mineral_import_sources.csv"


# Standardise mineral names across both datasets
def standardise_mineral(name):
    name = str(name).strip().lower()

    if "lithium" in name:
        return "Lithium"
    elif "nickel" in name:
        return "Nickel"
    elif "cobalt" in name:
        return "Cobalt"
    elif "manganese" in name:
        return "Manganese"
    elif "graphite" in name:
        return "Graphite"

    return None


print("Reading USGS import datasets...")

# Read both datasets
fig2 = pd.read_csv(FIG2_FILE, encoding="cp1252")
fig3 = pd.read_csv(FIG3_FILE, encoding="cp1252")

# Clean column names
for df in [fig2, fig3]:
    df.columns = (
        df.columns
        .str.replace("ï»¿", "", regex=False)
        .str.strip()
    )

# Standardise mineral names
fig2["Mineral"] = fig2["Commodity"].apply(standardise_mineral)
fig3["Mineral"] = fig3["Commodity"].apply(standardise_mineral)

# Keep only our five minerals
fig2 = fig2[fig2["Mineral"].notna()].copy()
fig3 = fig3[fig3["Mineral"].notna()].copy()

# Get import reliance from Figure 2
reliance = fig2[
    ["Mineral", "Net_Import_Reliance_pct_2025"]
].copy()

# Rename for clarity
reliance.rename(
    columns={
        "Net_Import_Reliance_pct_2025":
        "Net_Import_Reliance_2025"
    },
    inplace=True
)

# Attach Figure 2 import reliance to Figure 3 records
result = fig3.merge(
    reliance,
    on="Mineral",
    how="left",
    validate="many_to_one"
)

# Standardise output columns
result.rename(
    columns={
        "Import_Source_2021_24": "Source_Category",
        "Percent": "Import_Share_Percent",
        "NIR": "NIR_Figure3",
        "Critical_Mineral": "Critical_Mineral_Flag"
    },
    inplace=True
)

# "Other" is an aggregate, not a country
result["Source_Country"] = result["Source_Category"].where(
    result["Source_Category"].str.strip().str.lower() != "other"
)

result["Source_Type"] = result["Source_Category"].apply(
    lambda x: "aggregate_other"
    if str(x).strip().lower() == "other"
    else "country"
)

# Add context
result["Importing_Country"] = "United States"
result["Data_Period"] = "2021-2024"

# Select final columns
final_columns = [
    "Mineral",
    "Importing_Country",
    "Source_Country",
    "Source_Category",
    "Source_Type",
    "Import_Share_Percent",
    "Net_Import_Reliance_2025",
    "NIR_Figure3",
    "Critical_Mineral_Flag",
    "Data_Period"
]

result = result[final_columns]

# Sort records
result.sort_values(
    by=["Mineral", "Source_Type", "Source_Country"],
    inplace=True,
    na_position="last"
)

# Save processed dataset
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

result.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# Display summary
print("\nIMPORT SOURCE CLEANING COMPLETED!")
print("-" * 45)

print("Total records:", len(result))
print("Unique minerals:", result["Mineral"].nunique())

print("\nRecords by mineral:")
print(result["Mineral"].value_counts())

print("\nAggregate 'Other' records:")
print((result["Source_Type"] == "aggregate_other").sum())

print("\nOutput saved at:")
print(OUTPUT_FILE)

print("\nFirst ten records:")
print(result.head(10).to_string(index=False))
