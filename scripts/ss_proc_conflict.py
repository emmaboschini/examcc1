import pandas as pd

# Step 1: Tell the script which file to open
input_file = "data/raw/ss_raw_conflict.csv"
output_file = "data/clean/ss_clean_conflict.csv"

print(f"Filtering {input_file} for South Sudan incidents...")

# Step 2: Load the data
# We use 'latin1' encoding because sometimes humanitarian data has special characters.
df = pd.read_csv(input_file, encoding='latin1')

# Step 3: Filter for South Sudan only
# We look at the 'Country' column and only keep rows that say 'South Sudan'.
ss_df = df[df['Country'] == 'South Sudan'].copy()

# Step 4: Keep only the columns we need
# We want to know: When, Where, What happened, and Who was involved.
columns_to_keep = [
    'Date',
    'Admin 1',
    'Location of event',
    'Reported Perpetrator',
    'Weapon Carried/Used',
    'Type of education facility',
    'Attacks on Schools',
    'Educators Killed',
    'Students Killed'
]

cleaned_df = ss_df[columns_to_keep].copy()

# Step 5: Save the result
cleaned_df.to_csv(output_file, index=False)

print(f"Success! Cleaned conflict data saved to: {output_file}")
print(f"Total incidents found in South Sudan: {len(cleaned_df)}")
