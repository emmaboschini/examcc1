# Data Inventory & Technical Citations

This project integrates diverse datasets to provide a holistic view of South Sudan's education landscape. All data is sourced from open repositories.

---

## 1. 👥 Demographic Context
**Source:** [WorldPop Hub (SSD)](https://www.worldpop.org/project/categories?id=3&l=SSD)
- **Dataset:** SSD 100m Gridded Population Estimates.
- **Used For:** Modeling the under-17 population distribution at the county (Admin 2) level.
- **Resolution:** 100m x 100m grid cells, aggregated to administrative shapes.

---

## 2. 🏫 Education Infrastructure
**Source:** [MoGEI EMIS via HDX](https://data.humdata.org/dataset/south-sudan-schools-and-enrollment-data)
- **Dataset:** 2019 Annual Education Census (Baseline).
- **Contents:** Official census of over 6,300 registered schools.
- **Used For:** Providing the structural baseline for national education facilities.
- **Processing:** Converted from raw Excel to geocoded Pipe-delimited CSV for web stability.

---

## 3. ⚔️ Conflict Incident Logging
**Source:** [Insecurity Insight - Education in Danger](https://data.humdata.org/dataset/south-sudan-violence-incidents-affecting-aid-operations-education-and-health-care)
- **Dataset:** Violence incidents affecting aid operations and education.
- **Timeframe:** 2024–2026.
- **Used For:** Calculating state-level risk metrics and populating the sidebar chronological logs.
- **Note on Precision:** While specific site descriptions are included in the logs, geographic visualization is performed at the **State level** to highlight regional risk trends.

---

## 4. 🗺️ Spatial & Boundary Files
**Source:** [geoBoundaries.org](https://www.geoboundaries.org/)
- **Datasets:** SSD-ADM1 (States) and SSD-ADM2 (Counties).
- **Format:** High-resolution GeoJSON.
- **Used For:** Drawing the choropleth maps and enabling the spatial filtering logic.

---

## 📊 Project Statistics (Current Build)
- **Mapped Facilities:** 4,861 geocoded schools.
- **Documented Attacks:** 47 major conflict events in the monitored period.
- **County Success Rate:** 78/79 counties successfully matched for population mapping (98.7%).
- **State Coverage:** 10/10 states included in risk assessment metrics.

---
### Technology Stack
- **Web Mapping:** Leaflet.js (v1.9.4)
- **Analysis:** Pandas (Python 3.12)
- **Hosting:** GitHub Pages
- **Styling:** Custom Vanilla CSS for sidebar and dashboard UI
