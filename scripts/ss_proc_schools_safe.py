import pandas as pd

input_file = 'data/clean/ss_clean_schools_geo.csv'
output_file = 'data/clean/ss_clean_schools_geo_safe.csv'

# Load the current cleaned file
df = pd.read_csv(input_file)

# Remove any commas from names and types to prevent JS split issues
df['Name'] = df['Name'].str.replace(',', ';')
df['Type'] = df['Type'].str.replace(',', ';')
df['State'] = df['State'].str.replace(',', ';')

# Save with a Pipe | delimiter to be ultra safe
df.to_csv(output_file, index=False, sep='|')

print(f"Created safe schools file with {len(df)} entries using | delimiter.")
