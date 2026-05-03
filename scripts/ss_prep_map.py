import pandas as pd
import json

# Load population data
pop = pd.read_csv('data/clean/ss_clean_population_u17.csv')

# Create a lookup dictionary
# Note: Since Admin2 now has "(Alternate Name)", we need to map the base name back to the value
pop_dict = {}
for _, row in pop.iterrows():
    full_name = row['Admin2']
    pop_value = row['Total_Under_17']
    
    # Store with the full name
    pop_dict[full_name] = pop_value
    
    # Also store with the base name (the part before the parenthesis) for matching
    base_name = full_name.split(' (')[0].strip()
    pop_dict[base_name] = pop_value

# Load geographic data
with open('data/raw/ss_admin2.geojson') as f:
    gj = json.load(f)

# Merge the population into the GeoJSON properties
matched_count = 0
for feature in gj['features']:
    name = feature['properties'].get('shapeName')
    # We match the name from the map with the dictionary
    if name in pop_dict:
        feature['properties']['population'] = int(pop_dict[name])
        matched_count += 1
    else:
        feature['properties']['population'] = 0

# Save the combined file
with open('data/clean/ss_map_data.geojson', 'w') as f:
    json.dump(gj, f)

print(f"Success! Created data/clean/ss_map_data.geojson. Matched {matched_count} counties.")
