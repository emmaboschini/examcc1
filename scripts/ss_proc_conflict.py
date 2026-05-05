import pandas as pd

# File Paths
input_conflict = "data/raw/ss_raw_conflict.csv"
input_kobo = "data/raw/ss_kobo_entries.csv"
output_file = "data/clean/ss_clean_conflict.csv"

print(f"Generating cleaned conflict report for South Sudan...")

# 1. Load Main Conflict Data
df_raw = pd.read_csv(input_conflict, encoding='latin1')
ss_raw = df_raw[df_raw['Country'] == 'South Sudan'].copy()

# 2. Load Kobo Entries if they exist
try:
    kobo_df = pd.read_csv(input_kobo)
    # Ensure columns match for concatenation
    # Kobo uses 'State' and 'Facility Name', Conflict uses 'Admin 1' and 'Location of event'
    kobo_mapped = kobo_df.rename(columns={
        'State': 'Admin 1',
        'Facility Name': 'Location of event',
        'Facility Type': 'Type of education facility'
    })
    combined_df = pd.concat([ss_raw, kobo_mapped], ignore_index=True)
except FileNotFoundError:
    combined_df = ss_raw

# 3. Select and Order High-Signal Columns
cols_to_keep = [
    'Date',
    'Admin 1',
    'Location of event',
    'Type of education facility',
    'Reported Perpetrator',
    'Educators Killed',
    'Students Killed',
    'Status'
]

# Only keep columns that actually exist in the final combined data
existing_cols = [c for c in cols_to_keep if c in combined_df.columns]
final_df = combined_df[existing_cols].copy()

# 4. Final Tidying
final_df = final_df.sort_values('Date', ascending=False)
final_df['Status'] = final_df['Status'].fillna('verified')

# 5. Save
final_df.to_csv(output_file, index=False)

print(f"Success! Created {output_file} with {len(final_df)} total incidents (Verified + Field Updates).")
