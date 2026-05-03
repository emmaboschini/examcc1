# Data Inventory: South Sudan Risk Analysis

This document provides a detailed list of all open-source data assets used in this project.

---

## 1. Demographic Data
**Source:** [WorldPop (University of Southampton)](https://www.worldpop.org/project/categories?id=3&l=SSD)
- **Content:** High-resolution population counts for children under 17.
- **Used For:** Providing the neutral background layer for human context.

---

## 2. Education Infrastructure
**Source:** [Official EMIS database via OCHA/HDX Mirror](https://data.humdata.org/dataset/811c4282-2223-4fc9-9b40-43223c4e3c3e)
- **Content:** Official census of over 6,000 schools, including facility names and types.
- **Used For:** Identifying the locations and levels (Primary/Secondary) of schools nationwide.

---

## 3. Conflict Incident Data
**Source:** [Insecurity Insight - Education in Danger](https://data.humdata.org/dataset/south-sudan-violence-incidents-affecting-aid-operations-education-and-health-care)
- **Content:** Documented violence affecting schools, students, and educators (2024-2026).
- **Used For:** Assessing the safety and risk levels of educational facilities.

---

## 4. Geographic Boundaries
**Source:** [geoBoundaries.org (william & Mary geoLab)](https://www.geoboundaries.org/)
- **Content:** ADM1 (State) and ADM2 (County) digital boundary files (GeoJSON).
- **Used For:** Drawing the map shapes and enabling the regional filtering system.

---

## 5. Basemap & Technology
- **Leaflet.js:** Open-source JavaScript library for interactive maps.
- **CartoDB Light:** Professional, minimalist map background for maximum readability.
- **Pandas (Python):** Used for data cleaning and merging.

---
### Final Data Statistics
- **Schools Mapped:** 4,861 geocoded facilities.
- **Reported Incidents:** 47 major conflict events (2024-2026).
- **Population Resolution:** 100m x 100m grid estimates.
