
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FOLDER = PROJECT_ROOT / "data" / "processed"

# File paths
minerals_file = DATA_FOLDER / "ev_minerals.csv"
sources_file = DATA_FOLDER / "mineral_import_sources.csv"
applications_file = DATA_FOLDER / "mineral_applications.csv"

expected_minerals = {
    "Lithium",
    "Nickel",
    "Cobalt",
    "Manganese",
    "Graphite"
}

print("=" * 60)
print("ATMOGRAPH - PROCESSED DATA VALIDATION")
print("=" * 60)

# Check that all files exist
for file in [minerals_file, sources_file, applications_file]:
    if not file.exists():
        raise FileNotFoundError(f"Missing file: {file}")

print("\nAll three processed files found!")

# Load datasets
minerals = pd.read_csv(minerals_file, encoding="utf-8-sig")
sources = pd.read_csv(sources_file, encoding="utf-8-sig")
applications = pd.read_csv(applications_file, encoding="utf-8-sig")

# -------------------------------------------------
# 1. CHECK MINERAL DATASET
# -------------------------------------------------

print("\n1. EV MINERALS DATASET")

mineral_set = set(minerals["Mineral_Group"].dropna())

print("Total records:", len(minerals))
print("Unique minerals:", len(mineral_set))
print("Minerals:", sorted(mineral_set))

assert mineral_set == expected_minerals, "Mineral names do not match!"
assert len(minerals) == 5, "Unexpected number of mineral records!"
assert not minerals["Mineral_Group"].duplicated().any(), "Duplicate minerals found!"

print("EV minerals validation: PASSED")

# -------------------------------------------------
# 2. CHECK IMPORT SOURCE DATASET
# -------------------------------------------------

print("\n2. MINERAL IMPORT SOURCES")

source_set = set(sources["Mineral"].dropna())

print("Total records:", len(sources))
print("Unique minerals:", len(source_set))

assert source_set == expected_minerals, "Import source minerals do not match!"

# Check import percentages
sources["Import_Share_Percent"] = pd.to_numeric(
    sources["Import_Share_Percent"],
    errors="coerce"
)

assert sources["Import_Share_Percent"].notna().all(), \
    "Missing or invalid import percentages!"

assert sources["Import_Share_Percent"].between(0, 100).all(), \
    "Import percentages outside 0-100!"

# Check percentage totals for each mineral
print("\nImport percentage totals:")

for mineral, group in sources.groupby("Mineral"):
    total = group["Import_Share_Percent"].sum()

    print(f"{mineral}: {total:.1f}%")

    assert abs(total - 100) < 0.01, \
        f"Import percentages for {mineral} do not total 100!"

# Check Other category
other_rows = sources[
    sources["Source_Type"] == "aggregate_other"
]

assert len(other_rows) == 5, "Unexpected Other category count!"

assert other_rows["Source_Country"].isna().all(), \
    "Other category incorrectly assigned a country!"

print("Import sources validation: PASSED")

# -------------------------------------------------
# 3. CHECK MINERAL APPLICATIONS
# -------------------------------------------------

print("\n3. MINERAL APPLICATIONS")

application_set = set(applications["Mineral"].dropna())

print("Total records:", len(applications))
print("Unique minerals:", len(application_set))

assert application_set == expected_minerals, \
    "Application minerals do not match!"

assert len(applications) == 5, \
    "Unexpected number of application records!"

assert applications["Primary_Applications"].notna().all(), \
    "Missing application descriptions!"

print("Mineral applications validation: PASSED")

# -------------------------------------------------
# 4. FINAL SUMMARY
# -------------------------------------------------

print("\n" + "=" * 60)
print("FINAL VALIDATION SUMMARY")
print("=" * 60)

print("EV minerals: PASSED")
print("Import sources: PASSED")
print("Mineral applications: PASSED")

print("\nAll five minerals are present in all three datasets.")
print("All import-source percentages total 100% per mineral.")
print("\nDATA VALIDATION COMPLETED SUCCESSFULLY!")
