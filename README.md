# South Sudan: Education Risk & Infrastructure Dashboard (2024-2026)

This repository hosts a professional analytical dashboard designed to visualize the intersection of demographic density, educational infrastructure, and conflict impact in South Sudan. It serves as a decision-support tool for humanitarian actors and researchers to assess the safety and accessibility of schools in active conflict zones.

## 🗺️ Interactive Map Capabilities

The dashboard ([Live View](https://emmaboschini.github.io/examcc1/)) is an interactive spatial tool built with Leaflet.js, featuring:

### 1. Multi-Layer Risk Analysis
- **Conflict Risk Indicators (Red):** Graded markers sized proportionally to the frequency of attacks. Hovering reveals specific risk levels (e.g., "Critical Threat Level").
- **Educational Facilities (Blue Dots):** Precise geocoded locations for over 4,800 schools.
- **Population Density (Blue Gradient):** A Choropleth layer showing concentrations of children under 17 across 79 counties, providing essential context for human impact.

### 2. Analytical Controls
- **Regional Focusing:** A state-level filter that automatically zooms the map and isolates facilities within that administrative area.
- **Infrastructure Filtering:** Toggle between **Primary**, **Secondary**, and **Pre-Primary** levels to analyze specific educational sectors.
- **Interactive Sidebar:** A dynamic chronological log that updates based on map selection, showing the **Date**, **Actor**, **Target**, and **Human Cost** of reported incidents.

---

## 🧠 Analytical Methodology & Data Notes

To provide an accurate assessment of risk, this project employs a specific multi-layered approach:

### Why include School Infrastructure?
We include the precise locations of thousands of school facilities to move beyond generic state-level warnings. By layering these locations over the areas with reported attacks, researchers can identify **specific facilities** that are physically exposed to high-risk environments. This intersection is crucial for prioritizing safety interventions and identifying gaps in infrastructure security.

### Spatial Precision of Conflict Data
It is important to note that the conflict incident data is mapped at the **Administrative State level (Admin 1)** rather than with exact GPS coordinates. While the individual records contain location descriptions, the map visualizes these as state-wide risk indicators. This approach is highly effective for highlighting regional "hotspots" and identifying which broader areas are becoming progressively more dangerous for educational activities.

---

## 📁 Repository Organization

The project follows a structured data pipeline to ensure transparency and reproducibility:

### `data/raw/`
The foundation of the project, containing untouched datasets from global monitoring groups:
- `ss_raw_population.csv`: Demographic projections (UN/OCHA).
- `ss_raw_schools.csv`: National education census (MoGEI).
- `ss_raw_conflict.csv`: Global "Education in Danger" logs (Insecurity Insight).
- `ss_admin1.geojson` & `ss_admin2.geojson`: Digital boundary files.

### `data/clean/`
Optimized and merged data ready for the web map:
- `ss_clean_population_u17.csv`: Filtered demographics with alternate naming support.
- `ss_clean_schools_geo_safe.csv`: Stabilized school list using Pipe (`|`) delimiters to prevent parsing errors.
- `ss_conflict_map_data.geojson`: Merged spatial data containing embedded conflict history logs.

### `scripts/`
Python automation for data maintenance:
- `ss_proc_population.py`: Processes and reformats demographic names.
- `ss_proc_schools_safe.py`: Generates the web-optimized facility list.
- `ss_prep_conflict_map.py`: Aggregates attacks by state and builds the risk metrics.

---

## 🛠️ Maintenance & Publishing

### To Update the Data:
1. Replace files in `data/raw/` with newer versions.
2. Run the processing scripts from the root directory:
   ```bash
   python3 scripts/ss_proc_population.py
   python3 scripts/ss_proc_schools_safe.py
   python3 scripts/ss_prep_conflict_map.py
   ```
3. Commit and push the changes to GitHub.

### To Publish Changes:
The project is hosted via **GitHub Pages**. Any push to the `main` branch will automatically update the live dashboard.

---
*Developed for the South Sudan Humanitarian Data Project - May 2026*
