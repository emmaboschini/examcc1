# South Sudan: Population, Education & Conflict Data

This repository contains a curated collection of open-source datasets focused on the intersection of population distribution, education facilities, and conflict impact in South Sudan (2024–2026).

## 📁 Repository Structure

The repository is organized into specific "clusters" to keep the data and logic separate:

### 1. `data/raw/`
Contains the original datasets exactly as they were downloaded from global sources.
- `ss_raw_population.csv`: Full population projections.
- `ss_raw_schools.csv`: Official government school census.
- `ss_raw_conflict.csv`: Global "Education in Danger" dataset.

### 2. `data/clean/`
Contains simplified and processed files that are easier to read and analyze.
- `ss_clean_population_u17.csv`: Focuses on children under 17.
- `ss_clean_schools.csv`: Simplified list of 6,000+ schools (Stats).
- `ss_clean_schools_geo.csv`: Geocoded school list used for mapping.
- `ss_clean_conflict.csv`: Filtered specifically for South Sudan events.

### 3. `scripts/`
Contains the Python scripts used to transform the "raw" data into "clean" data.
- `ss_proc_population.py`: Processes population data.
- `ss_proc_schools.py`: Processes EMIS school data.
- `ss_proc_conflict.py`: Filters and cleans conflict data.
- `ss_prep_map.py`: Merges geographic boundaries with population data for the map.

## 🗺️ Interactive Map

The project includes a professional interactive map (`index.html`) that visualizes the distribution of children under 17 across South Sudan.

### How to View the Map:
1. **Locally:** Open the `index.html` file in any web browser.
2. **Online:** This project is ready for **GitHub Pages**.

### How to Publish to GitHub Pages:
1. Push this repository to GitHub.
2. Go to **Settings** > **Pages**.
3. Under **Build and deployment**, set the source to **Deploy from a branch**.
4. Select the **main** branch and the **root (/)** folder.
5. Click **Save**. Your map will be live at `https://[your-username].github.io/[repo-name]/`.

---

## 🚀 Getting Started

If you are new to data analysis, follow these steps:

1. **Understand the Sources:** Read `sources.md` to see where the data comes from (UN, WorldPop, Ministry of Education).
2. **Explore the Clean Data:** Look inside the `data/clean/` folder. These files are ready for use in Excel or Google Sheets.
3. **Re-run the Processing:** To see how the cleaning works, run the scripts from the main folder:
   ```bash
   python3 scripts/ss_proc_population.py
   python3 scripts/ss_proc_schools.py
   python3 scripts/ss_proc_conflict.py
   ```

---
*Created for the South Sudan Data Project - May 2026*
