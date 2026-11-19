# USGS EV Battery Mineral Dataset – AtmoGraph

## 1. Overview

This document describes the selection, preprocessing, cleaning, and validation of the USGS mineral datasets prepared for the AtmoGraph project.

The dataset focuses on five important minerals used in battery-related applications:

- Lithium
- Nickel
- Cobalt
- Manganese
- Graphite

The objective is to organise information about these minerals, their applications, and the United States' import sources into structured CSV files that can support supply-chain analysis and future knowledge graph development.

**Geographical focus:** United States (US)

**Primary data source:** U.S. Geological Survey (USGS), Mineral Commodity Summaries 2026.

## 2. Dataset Selection

The USGS Mineral Commodity Summaries 2026 dataset was selected as the primary source because it provides information about mineral production, consumption, import reliance, and major import sources.

The project focuses on five minerals relevant to battery applications.

| Mineral | Battery-related applications |
|---|---|
| Lithium | Batteries |
| Nickel | Batteries and metallurgy |
| Cobalt | Batteries and metallurgy |
| Manganese | Batteries and metallurgy |
| Graphite | Batteries, fuel cells, and lubricants |

The application descriptions are based on the USGS end-use data. They are not limited exclusively to electric vehicle batteries.

## 3. Raw Dataset Structure

The original USGS CSV files are stored in:

`graph_engineering/data/raw/USGS_MCS_2026/`

The six source files used for inspection and preparation are:

1. `MCS2026_Commodities_Data.csv`
2. `MCS2026_Fig2_Net_Import_Reliance.csv`
3. `MCS2026_Fig3_Major_Import_Sources.csv`
4. `MCS2026_T4_Country_Export_Control.csv`
5. `MCS2026_T6_Critical_Minerals_End_Use.csv`
6. `MCS2026_T7_Critical_Minerals_Salient.csv`

These files contain information about mineral statistics, net import reliance, import sources, export controls, mineral applications, and salient statistics.

## 4. Dataset Inspection

All six raw CSV files were inspected using Python and Pandas.

The following checks were performed:

- Number of rows and columns.
- Column names and data types.
- Missing values.
- Duplicate records.
- Sample records.
- Relevant mineral information.

### 4.1 Raw Dataset Summary

| Source file | Rows | Columns |
|---|---:|---:|
| Commodities Data | 8,886 | 12 |
| Fig 2 – Net Import Reliance | 68 | 6 |
| Fig 3 – Major Import Sources | 191 | 6 |
| T4 – Country Export Control | 19 | 5 |
| T6 – Critical Minerals End Use | 60 | 4 |
| T7 – Critical Minerals Salient | 39 | 17 |

No duplicate rows were identified in the six inspected source files.

Some columns contain missing values because not every statistic is reported for every mineral. These missing values were inspected rather than automatically replaced with zero.

## 5. Data Preprocessing

Python and Pandas were used to extract relevant records and create structured datasets.

The preprocessing activities included:

1. Loading the original CSV files.
2. Cleaning column names and removing the UTF-8 BOM marker where present.
3. Selecting the five target minerals.
4. Extracting relevant mineral statistics.
5. Preparing mineral import-source records.
6. Extracting mineral application information.
7. Saving the processed datasets in CSV format.

The original raw files were preserved without modification.

### 5.1 Encoding and Missing Values

The original USGS files were read using the `cp1252` encoding where required.

Processed CSV files were saved using `utf-8-sig` encoding.

Missing values were not automatically treated as zero. Special USGS values such as `W`, `E`, and `>50` were also not interpreted as ordinary numeric values without considering their original meaning.

## 6. Processed Dataset Structure

The processed files are stored in:

`graph_engineering/data/processed/`

Three datasets were generated.

### 6.1 ev_minerals.csv

This file contains the selected mineral records and their relevant production, consumption, and import-reliance information.

- Total records: 5
- Unique minerals: 5

Target minerals:
- Lithium
- Nickel
- Cobalt
- Manganese
- Graphite

### 6.2 mineral_import_sources.csv

This file contains the import-source distribution for the selected minerals.

- Total records: 23
- Unique minerals: 5

The dataset contains source-country information and the corresponding import percentages.

| Mineral | Import source | Import share |
|---|---|---:|
| Cobalt | Norway | 26% |
| Cobalt | Finland | 16% |
| Cobalt | Canada | 14% |
| Cobalt | Japan | 14% |
| Cobalt | Other | 30% |
| Graphite | China | 46% |
| Graphite | Canada | 13% |
| Graphite | Mozambique | 13% |
| Graphite | Mexico | 12% |
| Graphite | Other | 16% |
| Lithium | Chile | 54% |
| Lithium | Argentina | 43% |
| Lithium | Other | 3% |
| Manganese | Gabon | 23% |
| Manganese | South Africa | 21% |
| Manganese | Malaysia | 11% |
| Manganese | Australia | 10% |
| Manganese | Other | 35% |
| Nickel | Canada | 44% |
| Nickel | Norway | 11% |
| Nickel | Australia | 8% |
| Nickel | Brazil | 7% |
| Nickel | Other | 30% |

The import-source percentages total 100% for each mineral.

The category `Other` represents an aggregated share and is not treated as an individual country.

### 6.3 mineral_applications.csv

This file contains the primary application information for the selected minerals.

- Total records: 5
- Unique minerals: 5

| Mineral | Primary applications |
|---|---|
| Cobalt | Batteries and metallurgy |
| Graphite | Batteries, fuel cells, and lubricants |
| Lithium | Batteries |
| Manganese | Batteries and metallurgy |
| Nickel | Batteries and metallurgy |

## 7. Data Validation

A separate Python validation script was developed to verify the processed CSV files.

The validation script is:

`graph_engineering/src/data_preparation/validate_processed_data.py`

The following checks were performed:

- All three processed CSV files exist.
- All five expected minerals are present.
- No duplicate mineral records exist in the mineral and application datasets.
- Import percentages are numeric and between 0 and 100.
- Import-source percentages total 100% for each mineral.
- Aggregated `Other` records do not contain an individual source-country name.
- Mineral application descriptions are present.

### 7.1 Validation Results

| Validation check | Result |
|---|---|
| EV minerals dataset | PASSED |
| Mineral import sources | PASSED |
| Mineral applications | PASSED |
| Five target minerals present | PASSED |
| Import shares total 100% | PASSED |

**Final validation status: DATA VALIDATION COMPLETED SUCCESSFULLY.**

## 8. Python Scripts Developed

The following scripts were developed and tested:

| Script | Purpose |
|---|---|
| `inspect_usgs.py` | Inspects the six raw USGS datasets |
| `create_ev_minerals.py` | Extracts the five target minerals |
| `create_mineral_import_sources.py` | Prepares mineral import-source records |
| `create_mineral_applications.py` | Extracts mineral application information |
| `validate_processed_data.py` | Validates all processed datasets |

All five scripts were executed successfully using Python.

## 9. Project Folder Structure

The dataset-related project files are organised as follows:

```text
graph_engineering/
│
├── data/
│   ├── raw/
│   │   ├── USGS_MCS_2026/
│   │   │   ├── MCS2026_Commodities_Data.csv
│   │   │   ├── MCS2026_Fig2_Net_Import_Reliance.csv
│   │   │   ├── MCS2026_Fig3_Major_Import_Sources.csv
│   │   │   ├── MCS2026_T4_Country_Export_Control.csv
│   │   │   ├── MCS2026_T6_Critical_Minerals_End_Use.csv
│   │   │   └── MCS2026_T7_Critical_Minerals_Salient.csv
│   │   │
│   │   └── news/
│   │       └── historical_disruptions_first_5.csv
│   │
│   └── processed/
│       ├── ev_minerals.csv
│       ├── mineral_import_sources.csv
│       └── mineral_applications.csv
│
├── src/
│   └── data_preparation/
│       ├── inspect_usgs.py
│       ├── create_ev_minerals.py
│       ├── create_mineral_import_sources.py
│       ├── create_mineral_applications.py
│       └── validate_processed_data.py
│
└── docs/
    └── usgs_ev_mineral_dataset.md
```

## 10. Dataset Limitations and Assumptions

The following limitations must be considered when using these datasets:

1. **Geographical scope:** The USGS import-source information describes United States mineral imports and import reliance. It does not represent the complete global supply chain.

2. **No direct supplier relationships:** The datasets do not provide verified company-to-company supplier relationships, factory connections, or specific EV manufacturer contracts.

3. **Broad mineral applications:** The application categories include uses beyond electric vehicle batteries. They should not be interpreted as exclusively EV-related.

4. **Aggregated import sources:** The `Other` category represents combined import sources and cannot be treated as a specific country.

5. **Different source values:** Some USGS tables report net import reliance using different representations. For example, lithium is represented as `>50` in one source and `50.0` in another. Original source values should be preserved and their differences documented.

6. **No assumed disruption connections:** A mineral import-source record does not prove that a particular port, company, or disruption directly affects that mineral's supply.

7. **Historical news limitations:** The separately collected news records require independent entity and relevance verification before being connected to specific minerals or supply-chain nodes.

These limitations are important to prevent unsupported relationships from being introduced into the AtmoGraph knowledge graph.

## 11. Future Integration with AtmoGraph

The processed datasets can support the initial construction of a mineral-focused supply-chain graph.

Potential graph entities include:

- Mineral
- Source Country
- Import Share
- Mineral Application
- Disruption Event
- Location

For example, a source-country relationship can represent a documented mineral import source and its reported import share.

The processed datasets can later be integrated with verified disruption records and additional supply-chain information.

Any graph relationship should retain its source and relevant time period. Relationships not supported by the available data must not be assumed.

## 12. Conclusion

The USGS Mineral Commodity Summaries 2026 datasets were inspected and processed to prepare a structured dataset covering five battery-related minerals.

Three processed CSV files were generated, and five Python scripts were successfully executed.

The validation script confirmed that all five minerals are present across the three processed datasets and that the import-source percentages total 100% for every mineral.

This work provides a documented data foundation for further supply-chain graph construction and disruption analysis within the AtmoGraph project.

## 13. Data Source

**Primary source:** U.S. Geological Survey (USGS), Mineral Commodity Summaries 2026.

Source files are retained in the project's `data/raw/USGS_MCS_2026/` directory.

The processed datasets are derived from these source files and should be interpreted according to the limitations described in this document.