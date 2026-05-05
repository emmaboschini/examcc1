# South Sudan: Education Risk & Infrastructure Dashboard (2024-2026)

This repository hosts a professional analytical dashboard designed as a direct technical response to the **Education Bridge Initiative (EBI)** Request for Proposals (RFP): *Strengthening Education Continuity in Conflict-Affected Regions*.

It serves as a decision-support tool that integrates high-resolution demographic density, official educational infrastructure, and chronological conflict logs to assess the safety and accessibility of schools in active crisis zones.

---

## 🗺️ Interactive Dashboard
**Live Analytical Portal:** [https://emmaboschini.github.io/examcc1/](https://emmaboschini.github.io/examcc1/)

### Multi-Layered Risk Assessment
- **Conflict Risk Indicators (Red):** Proportional markers visualizing the frequency and intensity of verified attacks on education.
- **Educational Infrastructure (Orange Dots):** Precise geocoded locations for over **4,800 validated schools** within South Sudan.
- **Demographic Context (Blue Gradient):** High-resolution mapping of the **Under-17 Population**, identifying concentrations of school-age children.
- **Updates from the Field (Blue Sidebar):** Real-time integration of unverified field reports for immediate situational awareness.

### Decision-Support Controls
- **Regional Isolation:** Administrative filters to zoom and focus analysis on specific states.
- **Sector Analysis:** Toggles to isolate Primary, Secondary, or Pre-Primary facilities.
- **Dynamic Chronology:** A synchronized sidebar providing the **Date**, **Location**, and **Facility Type** of reported incidents.

---

## 🧠 Strategic Response & Methodology

This project fulfills the core objectives outlined in the **EBI RFP (April 2026)**:

### 1. Innovative Use of AI
As requested in the RFP, this project leverages **Artificial Intelligence** as a force multiplier. The entire data pipeline—from the initial sourcing of open datasets to the development of the Leaflet-based analytical dashboard—was orchestrated and built using the **Gemini CLI AI agent**.

### 2. Integration with EBI Foundation
The inclusion of high-resolution **Under-17 Population** gradients validates the foundational work of the **Education Bridge Initiative**. EBI’s AI-driven demographic mapping acts as a critical substrate for identifying discrepancies between child concentrations and existing infrastructure.

### 3. Complementing Field Expertise
The dashboard provides a unified picture of conflict impact, allowing EBI field teams to contextualize their ground-level relationships within a broader geographic framework.

---

## 📁 Data & Technical Architecture

### Clustered File Structure
- **`data/raw/`**: Source datasets (UN/OCHA, MoGEI, Insecurity Insight).
- **`data/raw/ss_kobo_entries.csv`**: Dedicated storage for live field reports.
- **`data/clean/`**: Production-ready files with parsing-safe delimiters.
- **`scripts/`**: Python "engines" for automated maintenance and risk aggregation.

### Processing Pipeline
- `ss_update_bot.py`: Connects to Kobo API and synchronizes field reports.
- `ss_proc_population.py`: Harmonizes demographic data.
- `ss_proc_schools_safe.py`: Generates geocoded facility lists.
- `ss_prep_conflict_map.py`: Aggregates attacks by state into risk metrics.

---

## 🛠️ Maintenance & Deployment

### Field Reporting Integration (KoboToolbox)
For local teams in low-bandwidth or offline environments, we use **KoboToolbox** for real-time reporting.
- **Reporting Form:** [Education Incident Report](https://ee-eu.kobotoolbox.org/x/Ox8Mmfdc)
- **Synchronization:** Automated every **30 minutes** via GitHub Actions.

**Key Advantages for EBI Field Teams:**
*   **Offline Data Collection:** Teams can record incidents in remote areas without internet; data syncs automatically once a connection is re-established.
*   **Data Standardization:** Controlled dropdowns (e.g., State names) eliminate manual typos and ensure 100% compatibility with the analytical map.
*   **Immediate Situational Awareness:** Reduces the "information lag" between a field incident and headquarters' response by automating the data pipeline.
*   **Scalability:** The open-source nature of Kobo allows EBI to deploy an unlimited number of field reporters without additional licensing costs.

### Automated Updates
A dedicated **Update Bot** (`scripts/ss_update_bot.py`) performs the following:
1. Connects to the Kobo API to fetch new field reports.
2. Synchronizes new incidents with `data/raw/ss_kobo_entries.csv`.
3. Re-runs all processing scripts to update the live map.

### Manual Maintenance
To refresh the dashboard manually:
1. Replace/Update raw files in `data/raw/`.
2. Run the update bot:
   ```bash
   python3 scripts/ss_update_bot.py
   ```
3. Commit and push to `main`.

---
*Technical Response developed for the Education Bridge Initiative (EBI) - May 2026*
