import pandas as pd
import json
import re

# File Paths
input_pop = 'data/clean/ss_clean_population_u17.csv'
input_geo = 'data/raw/ss_admin2.geojson'
output_file = 'data/clean/ss_map_data.geojson'

# Load population data
pop = pd.read_csv(input_pop)

# Create a robust lookup dictionary
pop_dict = {}
for _, row in pop.iterrows():
    full_name = str(row['Admin2'])
    pop_value = row['Total_Under_17']
    
    # Standard names
    pop_dict[full_name.lower()] = pop_value
    base_name = full_name.split(' (')[0].strip().lower()
    pop_dict[base_name] = pop_value
    
    # Parenthetical names
    alt_match = re.search(r'\((.*?)\)', full_name)
    if alt_match:
        pop_dict[alt_match.group(1).strip().lower()] = pop_value

# Load geographic data
with open(input_geo) as f:
    gj = json.load(f)

# Merge with special case handling
matched_count = 0
for feature in gj['features']:
    name = feature['properties'].get('shapeName', '').strip().lower()
    
    # Manual overrides for naming conventions
    if name == 'raga' and 'raja' in pop_dict:
        feature['properties']['population'] = int(pop_dict['raja'])
        matched_count += 1
    elif name in pop_dict:
        feature['properties']['population'] = int(pop_dict[name])
        matched_count += 1
    else:
        # Default to 0 if not matched (e.g., disputed or new areas)
        feature['properties']['population'] = 0

# Save the combined file
with open(output_file, 'w') as f:
    json.dump(gj, f)

print(f"Success! Created {output_file}. Matched {matched_count} counties.")
