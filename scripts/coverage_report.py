import pandas as pd
import json

pop = pd.read_csv('data/clean/ss_clean_population_u17.csv')
with open('data/raw/ss_admin2.geojson') as f:
    gj = json.load(f)

# Extract and normalize names
def get_base_name(x):
    return x.split(' (')[0].strip().lower()

pop_names = set(pop['Admin2'].apply(get_base_name))
geo_names = set([f['properties']['shapeName'].lower() for f in gj['features']])

print('--- DATA COVERAGE REPORT ---')
print(f'Total Counties in Population File: {len(pop_names)}')
print(f'Total Counties on Map (GeoJSON): {len(geo_names)}')

missing_in_geo = pop_names - geo_names
missing_in_pop = geo_names - pop_names

if missing_in_geo:
    print(f'\n[!] Found in Population file but NOT on map: {missing_in_geo}')
else:
    print('\n[✓] All population records matched to the map.')

if missing_in_pop:
    print(f'[!] Found on Map but NO population data: {missing_in_pop}')
