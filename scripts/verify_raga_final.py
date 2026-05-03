import json
try:
    with open('data/clean/ss_map_data.geojson') as f:
        gj = json.load(f)
    for f in gj['features']:
        name = f['properties'].get('shapeName')
        if name == 'Raga':
            print(f"FOUND: {name}, Population: {f['properties'].get('population')}")
except Exception as e:
    print(f"Error: {e}")
