# USGS MCS 2026 – Filtered EV Battery Mineral Dataset

## 1. Overview

This folder contains six filtered CSV datasets derived from the **USGS Mineral Commodity Summaries (MCS) 2026** source files.

The datasets focus on five minerals relevant to the EV battery supply chain:

1. Lithium
2. Nickel
3. Cobalt
4. Manganese
5. Graphite

The purpose of this filtering is to provide the team with a smaller, focused dataset for supply-chain analysis and graph-based modelling in the AtmoGraph project.

## 2. Source

**Source:** U.S. Geological Survey (USGS) – Mineral Commodity Summaries 2026.

The original CSV files are stored in:

`graph_engineering/data/raw/USGS_MCS_2026/`

The filtered CSV files are stored in this folder.

## 3. Filtered Files

| File | Original Rows | Filtered Rows | Description |
|---|---:|---:|---|
| MCS2026_Commodities_Data.csv | 8,886 | 550 | Commodity statistics and related information |
| MCS2026_Fig2_Net_Import_Reliance.csv | 68 | 5 | Net import reliance and major import-source information |
| MCS2026_Fig3_Major_Import_Sources.csv | 191 | 23 | Import-source countries and their percentage shares |
| MCS2026_T4_Country_Export_Control.csv | 19 | 8 | Country export-control information mentioning target minerals |
| MCS2026_T6_Critical_Minerals_End_Use.csv | 60 | 5 | Primary applications of the selected minerals |
| MCS2026_T7_Critical_Minerals_Salient.csv | 39 | 5 | Salient statistics for the selected minerals |

## 4. Filtering Method

The datasets were filtered using Python and Pandas.

The filtering process:
- Reads the original USGS CSV files.
- Identifies records containing the five selected mineral names.
- Uses the appropriate mineral-related column in each file.
- Retains the original columns and matching records.
- Saves the filtered datasets as CSV files using UTF-8 encoding.

The filtering script is:

`graph_engineering/src/data_preparation/filter_usgs_datasets.py`

## 5. Validation

The filtered files were checked for:
- Successful file creation.
- Correct row counts.
- Presence of the selected mineral names.
- Relevant records in each dataset.

All six filtering operations completed successfully.

## 6. Important Data Notes and Limitations

1. **Graphite naming:** Graphite appears with variations such as "Graphite (Natural)", "GRAPHITE (NATURAL)", and "Graphite, natural" in different source files.

2. **T4 export-control records:** The `Commodity_Year` column contains descriptive text that may mention multiple minerals in a single record. The eight matching rows are relevant descriptions, not eight individual mineral records.

3. **Import-source data:** Import percentages describe the source data's reported import shares. They do not establish direct company-to-company supplier relationships.

4. **Other category:** Where the source contains "Other", it represents an aggregate of additional sources and must not be treated as an individual country.

5. **EV application limitation:** Some minerals have multiple applications beyond batteries. Their inclusion does not mean that all reported production or imports are exclusively used in EV batteries.

6. **Source-period limitation:** Figures and statistics retain the reporting periods specified by USGS. They should not be interpreted as live supply-chain information.

7. **Graph modelling:** Relationships between countries, minerals, companies, ports, and industries should only be created when supported by the available data or separately verified sources.

## 7. Project Usage

These filtered datasets can support:
- Mineral and country entity identification.
- Import-source analysis.
- Mineral application mapping.
- Supply-chain graph construction.
- Further integration with verified disruption-news records.

They are intended as a foundation for the AtmoGraph supply-chain analysis, not as a complete record of EV battery supplier relationships.

---

**Prepared for:** AtmoGraph – Supply Chain Ripple Effect Predictor  
**Data source:** USGS Mineral Commodity Summaries 2026  
**Target domain:** EV Battery Mineral Supply Chain