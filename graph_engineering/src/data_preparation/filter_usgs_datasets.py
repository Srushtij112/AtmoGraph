
from pathlib import Path
import re
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "USGS_MCS_2026"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "USGS_MCS_2026_Filtered"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Five target minerals and useful naming variations
MINERAL_PATTERNS = {
    "Lithium": [r"lithium"],
    "Nickel": [r"nickel"],
    "Cobalt": [r"cobalt"],
    "Manganese": [r"manganese"],
    "Graphite": [r"graphite"],
}

# File name and corresponding filtering column
FILES_TO_FILTER = {
    "MCS2026_Commodities_Data.csv": "Commodity",
    "MCS2026_Fig2_Net_Import_Reliance.csv": "Commodity",
    "MCS2026_Fig3_Major_Import_Sources.csv": "Commodity",
    "MCS2026_T4_Country_Export_Control.csv": "Commodity_Year",
    "MCS2026_T6_Critical_Minerals_End_Use.csv": "Critical_Mineral",
    "MCS2026_T7_Critical_Minerals_Salient.csv": "Critical_mineral",
}


def clean_column_names(df):
    """Remove BOM artifacts and extra spaces from headers."""
    df.columns = (
        df.columns.astype(str)
        .str.replace("ï»¿", "", regex=False)
        .str.strip()
    )
    return df


def filter_minerals(df, column):
    """Keep rows mentioning at least one target mineral."""

    if column not in df.columns:
        raise KeyError(
            f"Column '{column}' not found. "
            f"Available columns: {df.columns.tolist()}"
        )

    pattern = "|".join(
        rf"\b{term}\b"
        for terms in MINERAL_PATTERNS.values()
        for term in terms
    )

    mask = df[column].fillna("").astype(str).str.contains(
        pattern,
        case=False,
        regex=True
    )

    return df[mask].copy()


print("=" * 65)
print("ATMOGRAPH - USGS DATASET FILTERING")
print("=" * 65)

summary = []

for filename, filter_column in FILES_TO_FILTER.items():

    input_file = RAW_FOLDER / filename
    output_file = OUTPUT_FOLDER / filename

    print(f"\nProcessing: {filename}")

    if not input_file.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {input_file}"
        )

    df = pd.read_csv(
        input_file,
        encoding="cp1252",
        low_memory=False
    )

    df = clean_column_names(df)

    original_rows = len(df)

    filtered_df = filter_minerals(
        df,
        filter_column
    )

    filtered_df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    filtered_rows = len(filtered_df)

    print("Original rows:", original_rows)
    print("Filtered rows:", filtered_rows)
    print("Filtering column:", filter_column)
    print("Saved:", output_file.name)

    if filtered_rows == 0:
        print(
            "NOTE: No matching mineral records found. "
            "An empty CSV with headers was saved."
        )

    summary.append({
        "File": filename,
        "Original_Rows": original_rows,
        "Filtered_Rows": filtered_rows,
        "Filtering_Column": filter_column
    })


print("\n" + "=" * 65)
print("FILTERING SUMMARY")
print("=" * 65)

summary_df = pd.DataFrame(summary)
print(summary_df.to_string(index=False))

print("\nAll six filtering operations completed.")
print("Output folder:", OUTPUT_FOLDER)
