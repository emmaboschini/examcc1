import csv

def clean_number(text):
    """
    Cleans a string like ' 13,954 ' into an actual number (integer).
    If the text is empty or not a number, it returns 0.
    """
    if not text:
        return 0
    # Remove spaces and commas
    clean_text = text.strip().replace(',', '').replace('"', '')
    try:
        return int(clean_text)
    except ValueError:
        return 0

# The names of the files we are using
input_file = '../data/raw/raw_population 2024 (UNFPA).csv'
output_file = '../data/processed/population_under_17.csv'

# Open the original file to read it
with open(input_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # We will store our new data in this list
    processed_rows = []
    
    for row in reader:
        # Skip rows that don't have a county name (like the total row at the bottom)
        if not row['Admin2']:
            continue
            
        # 1. Get the numbers for children under 5
        m_under_5 = clean_number(row[' No. of Male\nchildren under 5 '])
        f_under_5 = clean_number(row[' No. of Female\nchildren under 5 '])
        
        # 2. Get the numbers for children aged 5 to 17
        m_5_to_17 = clean_number(row[' No. of Male children \naged 5 - 17 years '])
        f_5_to_17 = clean_number(row[' No. of Female \nchildren aged 5 - 17 years '])
        
        # 3. Add them all together to get the total population under 17
        total_under_17 = m_under_5 + f_under_5 + m_5_to_17 + f_5_to_17
        
        # 4. Create a new simple row for our map
        new_row = {
            'State': row['Admin1'],
            'County': row['Admin2'],
            'Pcode': row['Admin2_Pcode'],
            'Population_Under_17': total_under_17
        }
        processed_rows.append(new_row)

# Save the new data into a simplified CSV file
with open(output_file, mode='w', encoding='utf-8', newline='') as f:
    fieldnames = ['State', 'County', 'Pcode', 'Population_Under_17']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(processed_rows)

print(f"Success! Created {output_file} with {len(processed_rows)} rows.")
