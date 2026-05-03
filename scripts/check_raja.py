import json
with open('data/clean/ss_map_data.geojson') as f:
    gj = json.load(f)
for f in gj['features']:
    name = f['properties'].get('shapeName', '')
    if 'raga' in name.lower() or 'raja' in name.lower():
        print(f"Name in GeoJSON: {name}, Population: {f['properties'].get('population')}")
