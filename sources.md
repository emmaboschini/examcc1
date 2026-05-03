# Data Sources

## 1. South Sudan Education Cluster Dataset
- **Provider:** Global Education Cluster (co-led by UNICEF and Save the Children)
- **Platform:** [Humanitarian Data Exchange (HDX)](https://data.humdata.org/) / [ReliefWeb](https://reliefweb.int/)
- **Description:** This dataset provides ground-level data on education in emergencies in South Sudan. It includes 5W (Who, What, Where, When, and for Whom) reporting, school functionality status, and reasons for school closures (including conflict and insecurity).
- **Local Files:**
    - `data/raw/raw_education in danger.csv`: The original, unedited dataset.
    - `data/processed/clean_education in danger.csv`: The processed and cleaned version of the dataset ready for analysis.

## 2. OpenStreetMap (OSM) School Data
- **Provider:** OpenStreetMap Contributors
- **Method:** Fetched via Overpass API
- **Description:** Geographic coordinates (latitude and longitude) and names of schools mapped in South Sudan. This provides the spatial context for the conflict analysis.
- **Local Files:**
    - `data/processed/south_sudan_schools.geojson`: GeoJSON file containing point data for 464 schools.
    - `scripts/fetch_osm_schools.py`: Python script used to query the Overpass API.

## 3. IOM DTM Baseline Assessment (Round 16)
- **Provider:** International Organization for Migration (IOM)
- **Platform:** [Humanitarian Data Exchange (HDX)](https://data.humdata.org/)
- **Description:** Displacement tracking data for IDPs and returnees across South Sudan. Collected between December 2024 and February 2025. Includes location-level data (Lat/Lon) and demographic estimates.
- **Local Files:**
    - `data/raw/iom_dtm_r16_baseline.xlsx`: The raw multi-sheet Excel dataset.
    - `data/processed/iom_dtm_r16_baseline.csv`: The converted data sheet for analysis.

## 4. OCHA Population Estimates 2024
- **Provider:** United Nations Office for the Coordination of Humanitarian Affairs (OCHA)
- **Platform:** [Humanitarian Data Exchange (HDX)](https://data.humdata.org/)
- **Description:** Official subnational population statistics for South Sudan, projected for 2024. Includes age-disaggregated data (e.g., ages 5-17 for school-age estimates) at the county level (Admin 2).
- **Local Files:**
    - `data/raw/ssd_2024_population_estimates.xlsx`: The raw Excel projections.
    - `data/processed/ssd_2024_population_estimates.csv`: Full CSV version.
    - `data/processed/school_age_population_2024.csv`: Filtered version with only school-age children (0-17).
    - `scripts/filter_school_age.py`: Script used to filter and transform the population data.
