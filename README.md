# South Sudan Population Map (Under 17)

This project provides an interactive map showing the population distribution of children and youth (under 17 years old) across South Sudan's counties.

## Data Source
The data is based on the **2024 Population Estimation Survey** (released 2023) by the South Sudan National Bureau of Statistics and processed using UNFPA projections for 2025.

## How it was built
- **Data Processing**: A Python script was used to sum the male and female population groups for ages 0-5 and 5-17 from the raw UNFPA dataset.
- **Mapping**: Built with [Leaflet.js](https://leafletjs.com/), a professional and lightweight mapping library.
- **Boundaries**: County borders (GeoJSON) are provided by [geoBoundaries](https://www.geoboundaries.org/).

## How to view
This map is designed to be published via **GitHub Pages**. 

1. Go to your GitHub repository settings.
2. Select **Pages** on the left sidebar.
3. Under **Branch**, select `main` and `/ (root)`.
4. Click **Save**.
