import json
import pandas as pd

print("Checking Conflict CSV...")
df = pd.read_csv('data/clean/ss_clean_conflict.csv')
print(f"Total rows in clean conflict CSV: {len(df)}")
print("States in CSV:", df['Admin 1'].unique())

print("\nChecking GeoJSON Map Data...")
with open('data/clean/ss_conflict_map_data.geojson') as f:
    gj = json.load(f)

for f in gj['features']:
    name = f['properties']['shapeName']
    incidents = f['properties'].get('incident_list', [])
    count = f['properties'].get('incidents_count', 0)
    print(f"{name}: {len(incidents)} in list, {count} in count property")
