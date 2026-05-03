import pandas as pd

# Step 1: Tell the script which file to open
input_file = "data/raw/ss_raw_population.csv"
output_file = "data/clean/ss_clean_population_u17.csv"

print(f"Reading {input_file}...")

# Step 2: Load the data
# We use 'pandas', a powerful tool for working with tables.
# We also use 'skipfooter=2' because the last two lines are empty or totals.
df = pd.read_csv(input_file, skipfooter=2, engine='python')

# Step 3: Select columns and combine names
# We read the alternate name to combine it for clarity if it differs from the primary name.
def combine_names(row):
    primary = str(row['Admin2']).strip()
    alternate = str(row['Admin2_Alternate_Name']).strip()
    if alternate and alternate != 'nan' and alternate != primary:
        return f"{primary} ({alternate})"
    return primary

# Create the clean dataframe
clean_df = df.copy()
clean_df['Admin2_Combined'] = clean_df.apply(combine_names, axis=1)

# Step 4: Keep only the columns we want
columns_to_keep = [
    'Admin1', 
    'Admin2_Combined',
    'Population - 2025',
    ' No. of Male\nchildren under 5 ',
    ' No. of Female\nchildren under 5 ',
    ' No. of Male children \naged 5 - 17 years ',
    ' No. of Female \nchildren aged 5 - 17 years '
]

filtered_df = clean_df[columns_to_keep].copy()
filtered_df = filtered_df.rename(columns={'Admin2_Combined': 'Admin2'})

# Step 5: Clean up the data
# The numbers in the CSV have commas (like "145,358") and extra spaces. 
# We need to remove them so the computer can treat them as real numbers.
columns_to_clean = [
    'Population - 2025',
    ' No. of Male\nchildren under 5 ',
    ' No. of Female\nchildren under 5 ',
    ' No. of Male children \naged 5 - 17 years ',
    ' No. of Female \nchildren aged 5 - 17 years '
]

for col in columns_to_clean:
    # Remove spaces and commas, then convert to numbers
    filtered_df[col] = filtered_df[col].astype(str).str.replace(',', '').str.strip()
    filtered_df[col] = pd.to_numeric(filtered_df[col], errors='coerce')

# Step 6: Calculate the Total Under 17
# We add up all the male and female children from both age groups.
filtered_df['Total_Under_17'] = (
    filtered_df[' No. of Male\nchildren under 5 '] + 
    filtered_df[' No. of Female\nchildren under 5 '] + 
    filtered_df[' No. of Male children \naged 5 - 17 years '] + 
    filtered_df[' No. of Female \nchildren aged 5 - 17 years ']
)

# Step 7: Save the result
filtered_df.to_csv(output_file, index=False)

print(f"Success! The filtered data has been saved to: {output_file}")
print("This file contains geography info and the total count of children under 17 (with alternate names in parentheses).")
