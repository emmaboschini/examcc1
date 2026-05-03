# South Sudan School Conflict Analysis

This project focuses on analyzing conflict incidents in schools across South Sudan, utilizing data from the South Sudan Education Cluster to identify trends, impacts, and areas of high risk.

## Project Overview
The primary goal is to understand the nature and frequency of conflict-related disruptions to education in South Sudan, including school closures, military use of facilities, and direct attacks.

## Data Sources
- **South Sudan Education Cluster Dataset**: Ground-level data on education in emergencies, including school functionality and conflict-related closures.
- Detailed source documentation can be found in [sources.md](./sources.md).

## Project Structure
- `data/raw/raw_education in danger.csv`: Original dataset as downloaded.
- `data/raw/iom_dtm_r16_baseline.xlsx`: IOM DTM Baseline Assessment Round 16 (Displacement data).
- `data/processed/iom_dtm_r16_baseline.csv`: CSV version of the IOM DTM dataset.
- `data/processed/clean_education in danger.csv`: Processed and cleaned data prepared for analysis.
- `data/processed/south_sudan_schools.geojson`: Geographic locations of schools from OpenStreetMap.
- `scripts/fetch_osm_schools.py`: Script used to download data from OpenStreetMap.
- `sources.md`: Documentation of data origins and characteristics.
- `README.md`: Project overview and status (this file).

## Current Status
- [x] Identify primary data source (South Sudan Education Cluster).
- [x] Download raw data.
- [x] Data cleaning and preprocessing.
- [x] Fetch geographic school data from OpenStreetMap (Overpass API).
- [x] Tidy project structure (organized into `data/` and `scripts/`).
- [x] Acquire IDP and population data (IOM DTM Round 16).
- [ ] Exploratory Data Analysis (EDA).
- [ ] Visualization of conflict trends.
- [ ] Final report/insights generation.

## How to Use
1. Refer to `sources.md` for background on the data.
2. The analysis-ready data is located in the `data/processed/` folder.
