import pandas as pd

# Step 1: Tell the script which file to open
input_file = "data/raw/ss_raw_population.csv"
output_file = "data/clean/ss_clean_population_u17.csv"

print(f"Reading {input_file}...")

# Step 2: Load the data
# We use 'pandas', a powerful tool for working with tables.
# We also use 'skipfooter=2' because the last two lines are empty or totals.
df = pd.read_csv(input_file, skipfooter=2, engine='python')

# Step 3: Keep only the columns we want
# The original file has many columns for adults. We only want:
# - Geography (Admin1, Admin2)
# - Total Population
# - Children under 5
# - Children aged 5-17
columns_to_keep = [
    'Admin1', 
    'Admin2', 
    'Population - 2025',
    ' No. of Male\nchildren under 5 ',
    ' No. of Female\nchildren under 5 ',
    ' No. of Male children \naged 5 - 17 years ',
    ' No. of Female \nchildren aged 5 - 17 years '
]

# Create a new version of our table with only these columns
filtered_df = df[columns_to_keep].copy()

# Step 4: Clean up the data
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

# Step 5: Calculate the Total Under 17
# We add up all the male and female children from both age groups.
filtered_df['Total_Under_17'] = (
    filtered_df[' No. of Male\nchildren under 5 '] + 
    filtered_df[' No. of Female\nchildren under 5 '] + 
    filtered_df[' No. of Male children \naged 5 - 17 years '] + 
    filtered_df[' No. of Female \nchildren aged 5 - 17 years ']
)

# Step 6: Save the result
filtered_df.to_csv(output_file, index=False)

print(f"Success! The filtered data has been saved to: {output_file}")
print("This file contains geography info and the total count of children under 17.")
