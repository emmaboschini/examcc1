import pandas as pd
import json
import re

# Load population data
pop = pd.read_csv('data/clean/ss_clean_population_u17.csv')

# Create a robust lookup dictionary
pop_dict = {}
for _, row in pop.iterrows():
    full_name = str(row['Admin2'])
    pop_value = row['Total_Under_17']
    
    # 1. Store with the full name (e.g., "Raja (Raga)")
    pop_dict[full_name.lower()] = pop_value
    
    # 2. Store with the base name (e.g., "Raja")
    base_name = full_name.split(' (')[0].strip()
    pop_dict[base_name.lower()] = pop_value
    
    # 3. Store with the alternate name inside parentheses (e.g., "Raga")
    alt_match = re.search(r'\((.*?)\)', full_name)
    if alt_match:
        alt_name = alt_match.group(1).strip()
        pop_dict[alt_name.lower()] = pop_value

# Load geographic data
with open('data/raw/ss_admin2.geojson') as f:
    gj = json.load(f)

# Merge the population into the GeoJSON properties
matched_count = 0
for feature in gj['features']:
    name = feature['properties'].get('shapeName', '').strip().lower()
    
    # We match the name from the map with the dictionary (case-insensitive)
    if name in pop_dict:
        feature['properties']['population'] = int(pop_dict[name])
        matched_count += 1
    else:
        # Try a more fuzzy match if needed, but for now exact or parenthetical
        feature['properties']['population'] = 0

# Save the combined file
with open('data/clean/ss_map_data.geojson', 'w') as f:
    json.dump(gj, f)

print(f"Success! Created data/clean/ss_map_data.geojson. Matched {matched_count} counties.")
