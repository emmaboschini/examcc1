import pandas as pd
import json

# Step 1: Tell the script which files to open
input_file = "data/raw/ss_raw_conflict.csv"
geojson_file = "data/raw/ss_admin1.geojson"
output_file = "data/clean/ss_conflict_map_data.geojson"

print(f"Merging conflict summary into State GeoJSON...")

# Step 2: Load conflict data
df = pd.read_csv(input_file, encoding='latin1')

# Load Kobo entries if the file exists
kobo_file = "data/raw/ss_kobo_entries.csv"
try:
    kobo_df = pd.read_csv(kobo_file)
    df = pd.concat([df, kobo_df], ignore_index=True)
except FileNotFoundError:
    pass

ss_df = df[df['Country'] == 'South Sudan'].copy()

# Ensure Status column exists
if 'Status' not in ss_df.columns:
    ss_df['Status'] = 'verified'

# Clean state names
ss_df['Admin 1'] = ss_df['Admin 1'].str.replace(' State', '', regex=False).str.strip()

# Aggregated verified data goes into the state risk math
verified_ss = ss_df[ss_df['Status'] == 'verified'].copy()
# Field updates for the side box
field_updates_ss = ss_df[ss_df['Status'] == 'field_update'].copy()

# Aggregate by State
state_incidents = {}
for state in verified_ss['Admin 1'].unique():
    incidents = verified_ss[verified_ss['Admin 1'] == state][[
        'Date', 'Location of event', 'Reported Perpetrator', 'Type of education facility'
    ]].fillna('No Information').to_dict('records')
    state_incidents[state] = incidents

summary_df = verified_ss.groupby('Admin 1').agg({
    'Date': 'count',
    'Educators Killed': 'sum',
    'Students Killed': 'sum'
}).rename(columns={'Date': 'Incident_Count'}).reset_index()
summary_dict = summary_df.set_index('Admin 1').to_dict('index')

with open(geojson_file) as f:
    gj = json.load(f)

# Field updates for the sidebar
# We try to use the new column names if they exist, otherwise fallback
if 'Facility Name' in field_updates_ss.columns:
    field_updates = field_updates_ss[[
        'Date', 'Facility Name', 'State', 'Facility Type'
    ]].rename(columns={'Facility Name': 'Location of event', 'State': 'Admin 1', 'Facility Type': 'Type of education facility'}).fillna('No Information').to_dict('records')
else:
    field_updates = field_updates_ss[[
        'Date', 'Location of event', 'Admin 1', 'Type of education facility'
    ]].fillna('No Information').to_dict('records')

for feature in gj['features']:
    name = feature['properties'].get('shapeName')
    stats = summary_dict.get(name, {'Incident_Count': 0, 'Educators Killed': 0, 'Students Killed': 0})
    
    count = int(stats['Incident_Count'])
    feature['properties']['incidents_count'] = count
    feature['properties']['educators_killed'] = int(stats['Educators Killed'])
    feature['properties']['students_killed'] = int(stats['Students Killed'])
    feature['properties']['incident_list'] = state_incidents.get(name, [])
    
    if count == 0: risk_level = "No Recent Incidents"
    elif count < 5: risk_level = "Active Conflict Area"
    elif count < 10: risk_level = "High-Risk Zone"
    else: risk_level = "Critical Threat Level"
    feature['properties']['risk_level'] = risk_level

# Attach global field updates to the top-level of the geojson
gj['field_updates'] = field_updates

# Step 4: Save the result
with open(output_file, 'w') as f:
    json.dump(gj, f)

print(f"Success! Created {output_file} with conflict stats for each state.")
