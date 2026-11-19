
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "USGS_MCS_2026"
    / "MCS2026_T6_Critical_Minerals_End_Use.csv"
)

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_FOLDER / "mineral_applications.csv"

# Target minerals
target_minerals = {
    "lithium": "Lithium",
    "nickel": "Nickel",
    "cobalt": "Cobalt",
    "manganese": "Manganese",
    "graphite": "Graphite"
}

print("Reading USGS mineral applications dataset...")

# Read original dataset
df = pd.read_csv(INPUT_FILE, encoding="cp1252")

# Clean column names
df.columns = (
    df.columns
    .str.replace("ï»¿", "", regex=False)
    .str.strip()
)

# Standardise mineral names
df["Critical_Mineral"] = (
    df["Critical_Mineral"].astype("string").str.strip()
)

df["Mineral"] = (
    df["Critical_Mineral"].str.lower().map(target_minerals)
)

# Select only target minerals
cleaned_df = df[df["Mineral"].notna()].copy()

# Select useful columns
cleaned_df = cleaned_df[
    [
        "Mineral",
        "Critical_Mineral",
        "Primary_Applications",
        "Category_Note"
    ]
]

# Add source information
cleaned_df["Data_Source"] = "USGS MCS 2026"
cleaned_df["Source_File"] = "MCS2026_T6_Critical_Minerals_End_Use.csv"

# Remove exact duplicate rows, if any
cleaned_df.drop_duplicates(inplace=True)

# Arrange records alphabetically
cleaned_df.sort_values(
    by="Mineral",
    inplace=True
)

# Save processed dataset
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

cleaned_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# Display results
print("\nMINERAL APPLICATION CLEANING COMPLETED!")
print("-" * 45)

print("Total records:", len(cleaned_df))
print("Unique minerals:", cleaned_df["Mineral"].nunique())

print("\nExtracted applications:")
print(
    cleaned_df[
        ["Mineral", "Primary_Applications"]
    ].to_string(index=False)
)

print("\nOutput saved at:")
print(OUTPUT_FILE)

print("\nComplete cleaned dataset:")
print(cleaned_df.to_string(index=False))
