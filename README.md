# South Sudan: Education Infrastructure & Risk Analysis (2024-2026)

This repository hosts a professional interactive web application designed to assess the risk facing educational facilities in South Sudan. It integrates population data, official school census records, and documented conflict incidents into a single analytical tool.

## 🗺️ Interactive Map Features

The map (`index.html`) is built using Leaflet.js and offers several layers of analysis:

- **Conflict Risk Indicators (Red):** Graded markers showing states targeted by violence. The marker size is proportional to the number of incidents.
- **School Facilities (Blue):** Precise locations of 4,800+ educational facilities across the country.
- **Population Context (Neutral):** A subtle backdrop showing the density of children under 17, used as a secondary reference layer.
- **Dynamic Sidebar:** A real-time data panel that displays a chronological history of attacks, perpetrator details, and casualty statistics for selected regions.

### Interactive Controls:
- **Administrative Filter:** Focus the map on a specific state to instantly zoom and filter facilities.
- **School Level Filter:** Toggle between Primary, Secondary, and Pre-Primary facilities to analyze specific infrastructure types.
- **Layer Control:** Turn individual data layers on or off to reduce clutter.

---

## 📁 Repository Structure

The project is organized into professional clusters:

### 1. `data/raw/`
Original, untouched datasets from global providers.
- `ss_raw_population.csv`: UN/OCHA population projections.
- `ss_raw_schools.csv`: MoGEI EMIS school census.
- `ss_raw_conflict.csv`: Insecurity Insight conflict logs.
- `ss_admin1.geojson` & `ss_admin2.geojson`: Geographic boundaries.

### 2. `data/clean/`
Processed files optimized for web mapping and analysis.
- `ss_clean_population_u17.csv`: Filtered demographic data.
- `ss_clean_schools_geo_safe.csv`: Geocoded school list (Pipe-delimited for stability).
- `ss_clean_conflict.csv`: South Sudan-specific incident list.
- `ss_conflict_map_data.geojson`: Merged spatial data with conflict risk metrics.

### 3. `scripts/`
Python "engines" used to transform and merge the data.
- `ss_proc_population.py`: Processes demographics.
- `ss_proc_schools_safe.py`: Creates the web-safe facility list.
- `ss_proc_conflict.py`: Filters global conflict logs.
- `ss_prep_map.py` & `ss_prep_conflict_map.py`: Prepare spatial data for the web map.

---

## 🚀 Getting Started & Publishing

1. **Local View:** Open `index.html` in any modern web browser.
2. **GitHub Pages:** This project is ready for automated hosting.
   - Go to **Settings** > **Pages** in your GitHub repo.
   - Select the **main** branch and **root (/)** folder.
   - Click **Save** to launch your live analytical map.

---
*Created for the South Sudan Data Project - May 2026*
