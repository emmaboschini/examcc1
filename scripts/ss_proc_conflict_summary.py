import pandas as pd

# Step 1: Tell the script which file to open
input_file = "data/raw/ss_raw_conflict.csv"
output_file = "data/clean/ss_clean_conflict_summary.csv"

print(f"Aggregating {input_file} by State for South Sudan...")

# Step 2: Load the data
df = pd.read_csv(input_file, encoding='latin1')

# Step 3: Filter for South Sudan only
ss_df = df[df['Country'] == 'South Sudan'].copy()

# Step 4: Group by State (Admin 1) and count the number of incidents
# We also count total fatalities (Educators + Students)
conflict_summary = ss_df.groupby('Admin 1').agg({
    'Date': 'count',
    'Educators Killed': 'sum',
    'Students Killed': 'sum'
}).rename(columns={'Date': 'Incident_Count'}).reset_index()

# Clean state names (e.g., "Jonglei State" -> "Jonglei" to match our other data)
conflict_summary['Admin 1'] = conflict_summary['Admin 1'].str.replace(' State', '', regex=False).strip()

# Step 5: Save the result
conflict_summary.to_csv(output_file, index=False)

print(f"Success! Summary saved to: {output_file}")
print(conflict_summary)
