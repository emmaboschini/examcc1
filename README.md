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

- **Hosting:** Deployed via **GitHub Pages** for instant accessibility by non-technical staff.
- **Updates:** To refresh the dashboard, simply replace raw files and run the processing scripts. All spatial logic is automated to handle changing conflict dynamics.

---
*Technical Response developed for the Education Bridge Initiative (EBI) - May 2026*
