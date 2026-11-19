
from pathlib import Path
import pandas as pd

# Project folder: graph_engineering
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input and output paths
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "USGS_MCS_2026"
    / "MCS2026_T7_Critical_Minerals_Salient.csv"
)

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_FOLDER / "ev_minerals.csv"

# Five target EV battery minerals
mineral_mapping = {
    "lithium": "Lithium",
    "nickel": "Nickel",
    "cobalt": "Cobalt",
    "manganese": "Manganese",
    "graphite (natural)": "Graphite"
}

print("Reading USGS dataset...")

# Read original dataset
df = pd.read_csv(INPUT_FILE, encoding="cp1252")

# Clean column names
df.columns = (
    df.columns
    .str.replace("ï»¿", "", regex=False)
    .str.strip()
)

# Remove unnecessary spaces from mineral names
df["Critical_mineral"] = (
    df["Critical_mineral"].astype("string").str.strip()
)

# Select only our five target minerals
df["Mineral_Group"] = (
    df["Critical_mineral"].str.lower().map(mineral_mapping)
)

cleaned_df = df[df["Mineral_Group"].notna()].copy()

# Put the standardised mineral name first
columns = ["Mineral_Group"] + [
    col for col in cleaned_df.columns
    if col != "Mineral_Group"
]

cleaned_df = cleaned_df[columns]

# Create output folder if it doesn't exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Save cleaned dataset
cleaned_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

# Display results
print("\nDATA CLEANING COMPLETED!")
print("-" * 45)
print("Original rows:", len(df))
print("Selected rows:", len(cleaned_df))
print("Unique minerals:", cleaned_df["Mineral_Group"].nunique())
print("\nMinerals included:")
print(cleaned_df["Mineral_Group"].value_counts())
print("\nOutput saved at:")
print(OUTPUT_FILE)

print("\nFirst five records:")
print(cleaned_df.head().to_string(index=False))
