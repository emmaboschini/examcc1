import pandas as pd
import json

# Step 1: Tell the script which files to open
input_file = "data/raw/ss_raw_conflict.csv"
geojson_file = "data/raw/ss_admin1.geojson"
output_file = "data/clean/ss_conflict_map_data.geojson"

print(f"Merging conflict summary into State GeoJSON...")

# Step 2: Load conflict data
df = pd.read_csv(input_file, encoding='latin1')
ss_df = df[df['Country'] == 'South Sudan'].copy()

# Ensure Status column exists
if 'Status' not in ss_df.columns:
    ss_df['Status'] = 'verified'

# Clean state names
ss_df['Admin 1'] = ss_df['Admin 1'].str.replace(' State', '', regex=False).str.strip()

# --- NEW: Separate Verified vs Unverified ---
# Verified data goes into the state risk math
verified_ss = ss_df[ss_df['Status'] == 'verified'].copy()
# Unverified news alerts for individual dots
unverified_ss = ss_df[ss_df['Status'] == 'unverified'].copy()

# Aggregate by State (VERIFIED ONLY)
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

# Step 3: Load GeoJSON and merge data
with open(geojson_file) as f:
    gj = json.load(f)

# Keep track of unverified news for the map
news_alerts = unverified_ss[[
    'Date', 'Location of event', 'Source URL', 'Type of education facility'
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

# Save the news alerts in a separate property or file
# We will attach the global news alerts to the top-level of the geojson
gj['news_alerts'] = news_alerts

# Step 4: Save the result
with open(output_file, 'w') as f:
    json.dump(gj, f)

print(f"Success! Created {output_file} with conflict stats for each state.")
