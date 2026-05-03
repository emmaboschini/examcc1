import pandas as pd
import json

# Load population data
pop = pd.read_csv('data/clean/ss_clean_population_u17.csv')

# Load geographic data
with open('data/raw/ss_admin2.geojson') as f:
    gj = json.load(f)

# Create a dictionary for quick lookup: { "CountyName": PopulationValue }
pop_dict = pop.set_index('Admin2')['Total_Under_17'].to_dict()

# Merge the population into the GeoJSON properties
for feature in gj['features']:
    name = feature['properties'].get('shapeName')
    # We match the name from the map with the name in our CSV
    feature['properties']['population'] = int(pop_dict.get(name, 0))

# Save the combined file
with open('data/clean/ss_map_data.geojson', 'w') as f:
    json.dump(gj, f)

print("Success! Created data/clean/ss_map_data.geojson with population info.")
