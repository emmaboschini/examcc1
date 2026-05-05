# South Sudan: Education Risk & Infrastructure Dashboard (2024-2026)

This repository hosts a professional analytical dashboard designed as a direct technical response to the **Education Bridge Initiative (EBI)** Request for Proposals (RFP): *Strengthening Education Continuity in Conflict-Affected Regions*.

It serves as a decision-support tool that integrates high-resolution demographic density, official educational infrastructure, and chronological conflict logs to assess the safety and accessibility of schools in active crisis zones.

---

## 🗺️ Interactive Dashboard
**Live Analytical Portal:** [https://emmaboschini.github.io/examcc1/](https://emmaboschini.github.io/examcc1/)

### Multi-Layered Risk Assessment
- **Conflict Risk Indicators (Red):** Proportional markers visualizing the frequency and intensity of attacks on education.
- **Educational Infrastructure (Orange Dots):** Precise geocoded locations for over 4,800 schools, allowing for site-specific risk analysis.
- **Demographic Context (Blue Gradient):** High-resolution mapping of the **Under-17 Population**, identifying concentrations of school-age children in relation to infrastructure and conflict.

### Decision-Support Controls
- **Regional Isolation:** Administrative filters to zoom and focus analysis on specific states.
- **Sector Analysis:** Toggles to isolate Primary, Secondary, or Pre-Primary facilities.
- **Dynamic Chronology:** A real-time sidebar providing the **Date**, **Actor**, and **Target** of reported incidents, moving from data points to detailed narratives.

---

## 🧠 Strategic Response & Methodology

This project fulfills the core objectives outlined in the **EBI RFP (April 2026)**:

### 1. Innovative Use of AI
As requested in the RFP, this project leverages **Artificial Intelligence** as a force multiplier. The entire data pipeline—from the initial sourcing of open datasets to the development of the Leaflet-based analytical dashboard—was orchestrated and built using the **Gemini CLI AI agent**. This demonstrates how AI can improve the efficiency, scalability, and technical rigor of humanitarian data projects.

### 2. Integration with EBI Foundation
The inclusion of high-resolution **Under-17 Population** gradients validates the foundational work of the **Education Bridge Initiative**. We have demonstrated that EBI’s AI-driven demographic mapping acts as a critical substrate for identifying discrepancies between child concentrations and existing infrastructure.

### 3. Complementing Field Expertise
While the dashboard provides a broad regional overview, it is designed to **complement rather than replace** EBI's field teams. By providing headquarters with a unified picture of conflict impact, it allows local teams to contextualize their ground-level relationships within a broader geographic framework.

---

## 📁 Data & Technical Architecture

The project is built entirely on **open, publicly available data sources**, ensuring EBI can scale the tool without proprietary licensing costs.

### Clustered File Structure
- **`data/raw/`**: Source datasets (UN/OCHA, MoGEI, Insecurity Insight).
- **`data/clean/`**: Production-ready files with alternate naming support and parsing-safe delimiters.
- **`scripts/`**: Python "engines" for automated maintenance and risk aggregation.

### Processing Pipeline
- `ss_proc_population.py`: Harmonizes demographic data.
- `ss_proc_schools_safe.py`: Generates geocoded facility lists.
- `ss_prep_conflict_map.py`: Aggregates attacks by state into risk metrics.

---

## 🛠️ Maintenance & Deployment

### Field Reporting Integration (KoboToolbox)
For local teams in low-bandwidth or offline environments, we use **KoboToolbox** for real-time reporting.
- **Reporting Form:** [Education Incident Report](https://ee-eu.kobotoolbox.org/x/Ox8Mmfdc)
- **Synchronization:** Dropdowns are standardized to match map administrative logic.

### Automated Daily Updates
The dashboard is automated via **GitHub Actions**. Every 24 hours, a dedicated **Update Bot** (`scripts/ss_update_bot.py`) performs the following:
1. Connects to the Kobo API to fetch new field reports.
2. Synchronizes new incidents with the master database (`data/raw/ss_raw_conflict.csv`).
3. Re-runs all processing scripts to update the live map.

### Manual Maintenance
To refresh the dashboard manually:
1. Replace raw files in `data/raw/`.
2. Run the processing scripts:
   ```bash
   python3 scripts/ss_proc_population.py
   python3 scripts/ss_proc_schools_safe.py
   python3 scripts/ss_prep_conflict_map.py
   ```
3. Commit and push to `main`.

---
*Technical Response developed for the Education Bridge Initiative (EBI) - May 2026*
