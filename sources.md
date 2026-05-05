# Data Inventory & Technical Citations

This inventory documents the open-source data assets used to build the technical response for the **Education Bridge Initiative (EBI)** RFP.

---

## 1. 👥 Demographic Context (EBI Foundation)
**Source:** [WorldPop Hub (SSD)](https://www.worldpop.org/project/categories?id=3&l=SSD)
- **Dataset:** SSD 100m Gridded Population Estimates (2024-2026).
- **Alignment:** This layer validates the foundational demographic AI-mapping work performed by the **Education Bridge Initiative (EBI)**.
- **Used For:** Identifying concentrations of school-age children (Under 17) to assess discrepancies in educational access.

---

## 2. 🏫 Education Infrastructure
**Source:** [Official EMIS database via OCHA/HDX Mirror](https://data.humdata.org/dataset/south-sudan-schools-and-enrollment-data)
- **Dataset:** 2019 Annual Education Census (Baseline).
- **Contents:** Official census of over 6,300 registered schools.
- **Used For:** Providing the structural baseline for national education facilities across South Sudan.

---

## 3. ⚔️ Conflict Incident Logging
**Source:** [Insecurity Insight - Education in Danger](https://data.humdata.org/dataset/south-sudan-violence-incidents-affecting-aid-operations-education-and-health-care)
- **Dataset:** Violence incidents affecting aid operations and education.
- **Timeframe:** 2024–2026.
- **Used For:** Mapping regional risk trends and populating the dashboard's dynamic chronological logs.

---

## 4. 🗺️ Spatial & Boundary Files
**Source:** [geoBoundaries.org (William & Mary geoLab)](https://www.geoboundaries.org/)
- **Datasets:** SSD-ADM1 (States) and SSD-ADM2 (Counties).
- **Format:** High-resolution GeoJSON.
- **Used For:** Administrative filtering and Choropleth mapping.

---

## 📊 Project Statistics (Build: May 2026)
- **Geocoded Infrastructure:** 4,861 individual school facilities mapped.
- **Documented Incidents:** 47 high-impact conflict events (SSD Focus).
- **County Success Rate:** 98.7% (78/79 administrative counties successfully synchronized).
- **License Model:** 100% Open-Source (No proprietary licenses required per EBI objective).

---
### Technology Stack (EBI RFP Compliance)
- **AI Integration:** **Gemini CLI Agent** used for automated data processing and dashboard orchestration.
- **Geospatial Engine:** Leaflet.js (v1.9.4) for non-technical staff accessibility.
- **Data Engineering:** Python (Pandas 3.12) for maintainable data pipelines.
- **Hosting:** GitHub Pages (Public cloud deployment).
