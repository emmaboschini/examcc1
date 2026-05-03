# South Sudan: Education Risk & Infrastructure Dashboard (2024-2026)

This repository hosts a professional analytical dashboard designed to visualize the intersection of demographic density, educational infrastructure, and conflict impact in South Sudan. It serves as a decision-support tool for humanitarian actors and researchers to assess the safety and accessibility of schools in active conflict zones.

---

## 🗺️ Interactive Dashboard
**Explore the Live Map:** [https://emmaboschini.github.io/examcc1/](https://emmaboschini.github.io/examcc1/)

### Core Analytical Layers
- **Conflict Risk Indicators (Red):** Graded markers sized proportionally to the frequency of reported attacks.
- **Educational Facilities (Orange Dots):** Precise geocoded locations for over 4,800 schools.
- **Population Density (Blue Gradient):** A high-resolution layer showing concentrations of children under 17, providing essential demographic context.

### User Controls
- **Administrative Focusing:** State-level filter that automatically zooms the map and isolates local facilities.
- **Sector Filtering:** Toggle between **Primary**, **Secondary**, and **Pre-Primary** levels for targeted analysis.
- **Dynamic Chronology:** A sidebar log that updates in real-time to show the **Date**, **Actor**, and **Target** of reported incidents in selected regions.

---

## 🧠 Methodology & Strategic Context

### Response to the Building Bridges Initiative RFP
This dashboard is a direct strategic response to the **Request for Proposals (RFP)** issued by the **Building Bridges Initiative**. In their proposal, the Initiative highlighted their innovative use of **Artificial Intelligence** to map demographic concentrations in complex environments.

Our decision to include high-resolution **Under-17 Population** gradients demonstrates that their AI-driven mapping works as a powerful foundational layer for advanced risk analysis. By integrating their work with our conflict and infrastructure data, we show how these insights can be transformed into actionable humanitarian tools.

### Why include School Infrastructure?
We include precise facility locations to move beyond generic state-level warnings. By layering infrastructure over reported attacks, researchers can identify **specific schools** physically exposed to high-risk environments. This intersection is crucial for prioritizing safety interventions.

### Spatial Precision of Conflict Data
Conflict incident data is mapped at the **Administrative State level (Admin 1)**. While individual records contain specific location descriptions (available in the sidebar), the map visualizes regional "hotspots" to identify broader areas becoming progressively dangerous for educational activities.

---

## 📁 Repository & Data Architecture

The project follows a structured data pipeline to ensure transparency and reproducibility:

### Clustered File Structure
- **`data/raw/`**: Foundation datasets from global monitoring groups (UN/OCHA, MoGEI, Insecurity Insight).
- **`data/clean/`**: Optimized files, including demographics with alternate naming support and stabilized Pipe-delimited (`|`) school lists.
- **`scripts/`**: Python "engines" for data maintenance (Demographics, Safe CSV conversion, Risk aggregation).

### Processing Pipeline
- `ss_proc_population.py`: Harmonizes demographic names.
- `ss_proc_schools_safe.py`: Generates parsing-safe facility lists.
- `ss_prep_conflict_map.py`: Merges spatial boundaries with dynamic risk metrics.

---

## 🛠️ Technical Workflow

### Data Maintenance
To update the dashboard with new data:
1. Replace files in `data/raw/` with newer versions.
2. Run the processing scripts from the root directory.
3. Commit and push the changes to GitHub.

### Deployment
The project is hosted via **GitHub Pages**. Any push to the `main` branch automatically updates the live analytical dashboard.

---
*Developed for the South Sudan Humanitarian Data Project - May 2026*
