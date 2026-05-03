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

# Clean state names to match GeoJSON (e.g., remove " State")
ss_df['Admin 1'] = ss_df['Admin 1'].str.replace(' State', '', regex=False).str.strip()

# Aggregate by State and also keep individual incident details
state_incidents = {}
for state in ss_df['Admin 1'].unique():
    # Only keep relevant columns and ensure they are strings
    incidents = ss_df[ss_df['Admin 1'] == state][[
        'Date', 'Location of event', 'Reported Perpetrator', 'Type of education facility'
    ]].copy()
    
    # Fill empty values to prevent JS errors
    incidents = incidents.fillna('No Information')
    
    state_incidents[state] = incidents.to_dict('records')

# Create summary lookup
summary_df = ss_df.groupby('Admin 1').agg({
    'Date': 'count',
    'Educators Killed': 'sum',
    'Students Killed': 'sum'
}).rename(columns={'Date': 'Incident_Count'}).reset_index()
summary_dict = summary_df.set_index('Admin 1').to_dict('index')

# Step 3: Load GeoJSON and merge data
with open(geojson_file) as f:
    gj = json.load(f)

for feature in gj['features']:
    name = feature['properties'].get('shapeName')
    # Default values if no conflict found
    stats = summary_dict.get(name, {'Incident_Count': 0, 'Educators Killed': 0, 'Students Killed': 0})
    
    count = int(stats['Incident_Count'])
    feature['properties']['incidents_count'] = count
    feature['properties']['educators_killed'] = int(stats['Educators Killed'])
    feature['properties']['students_killed'] = int(stats['Students Killed'])
    feature['properties']['incident_list'] = state_incidents.get(name, [])
    
    # Dynamic Risk Level
    if count == 0:
        risk_level = "No Recent Incidents"
    elif count < 5:
        risk_level = "Active Conflict Area"
    elif count < 10:
        risk_level = "High-Risk Zone"
    else:
        risk_level = "Critical Threat Level"
    
    feature['properties']['risk_level'] = risk_level

# Step 4: Save the result
with open(output_file, 'w') as f:
    json.dump(gj, f)

print(f"Success! Created {output_file} with conflict stats for each state.")
