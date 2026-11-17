
from pathlib import Path
import pandas as pd

# Project folder: graph_engineering
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Folder containing our six original datasets
DATASET_FOLDER = (
    PROJECT_ROOT / "data" / "raw" / "USGS_MCS_2026"
)

# All CSV files in the folder
csv_files = sorted(DATASET_FOLDER.glob("*.csv"))

print("=" * 60)
print("USGS DATASET INSPECTION")
print("=" * 60)

for file_path in csv_files:

    print("\n\nFILE:", file_path.name)
    print("-" * 60)

    try:
        df = pd.read_csv(file_path, low_memory=False, encoding="cp1252")

        # 1. Dataset size
        print("\n1. DATASET SIZE")
        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])

        # 2. Column names
        print("\n2. COLUMN NAMES")
        for column in df.columns:
            print("-", column)

        # 3. Missing values
        print("\n3. MISSING VALUES")
        print(df.isnull().sum())

        # 4. Duplicate rows
        print("\n4. DUPLICATE ROWS")
        print(df.duplicated().sum())

        # 5. First five records
        print("\n5. FIRST FIVE RECORDS")
        print(df.head().to_string(index=False))

    except Exception as error:
        print("ERROR while reading file:", error)

print("\n\nInspection completed!")
