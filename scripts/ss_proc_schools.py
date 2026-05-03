import pandas as pd
import re

# Step 1: Load the raw EMIS data
input_file = "data/raw/ss_raw_schools.csv"
output_file = "data/clean/ss_clean_schools.csv"

print(f"Cleaning {input_file}...")

# Read the file
df = pd.read_csv(input_file)

# Step 2: Select only the most important columns
# We are removing the confusing codes (like _G3, _SID) and grade-by-grade breakdowns.
columns_to_keep = {
    '_G3': 'State',
    '_G2': 'County',
    '_G1': 'Payam',
    'School': 'School_Name',
    'Type': 'School_Type',
    'TOTP': 'Total_Primary_Students',
    'TOTS': 'Total_Secondary_Students',
    'TOTAL': 'Total_Students'
}

# Create a new table with only these columns and rename them
cleaned_df = df[list(columns_to_keep.keys())].rename(columns=columns_to_keep).copy()

# Step 3: Clean the School Names
# Many schools look like "Bari Primary [BRM]". We want to remove the "[BRM]" part.
def clean_school_name(name):
    if pd.isna(name):
        return name
    # This removes anything inside square brackets []
    return re.sub(r'\[.*?\]', '', str(name)).strip()

cleaned_df['School_Name'] = cleaned_df['School_Name'].apply(clean_school_name)

# Step 4: Handle missing numbers
# If a school has no data for a column, we'll put a 0 instead of leaving it blank.
numeric_cols = ['Total_Primary_Students', 'Total_Secondary_Students', 'Total_Students']
for col in numeric_cols:
    cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0).astype(int)

# Step 5: Save the clean version
cleaned_df.to_csv(output_file, index=False)

print(f"Success! Cleaned data saved to: {output_file}")
print(f"Total schools processed: {len(cleaned_df)}")
