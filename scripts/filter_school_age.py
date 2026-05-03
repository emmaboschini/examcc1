import pandas as pd
import os

def filter_school_age_data():
    """
    This script reads the population data and keeps only the information
    related to children under 17 years old.
    """
    
    # 1. Define the file paths
    # We use the file we downloaded earlier
    input_file = "data/processed/ssd_2024_population_estimates.csv"
    output_file = "data/processed/school_age_population_2024.csv"
    
    print(f"Reading {input_file}...")
    
    # 2. Load the data using pandas
    df = pd.read_csv(input_file)
    
    # 3. Identify the columns we want to keep
    # We want the County names (Admin2) and the columns that count children
    columns_to_keep = [
        'Admin1', 
        'Admin2', 
        'Admin2_Pcode', 
        'No. of Male\nchildren under 5', 
        'No. of Female\nchildren under 5', 
        'No. of Male children \naged 5 - 17 years', 
        'No. of Female \nchildren aged 5 - 17 years'
    ]
    
    # Filter the data to keep only these columns
    df_filtered = df[columns_to_keep]
    
    # 4. Simplify the column names (Cleaning)
    # The original names have newlines (\n) and are long. Let's make them pretty.
    new_names = {
        'No. of Male\nchildren under 5': 'Male_Under_5',
        'No. of Female\nchildren under 5': 'Female_Under_5',
        'No. of Male children \naged 5 - 17 years': 'Male_5_17',
        'No. of Female \nchildren aged 5 - 17 years': 'Female_5_17'
    }
    df_filtered = df_filtered.rename(columns=new_names)
    
    # 5. Transform the data from "Wide" to "Long"
    # Currently, each county has 4 columns for kids. 
    # To "keep only rows where age is under 17", we turn those columns into rows.
    df_long = pd.melt(
        df_filtered, 
        id_vars=['Admin1', 'Admin2', 'Admin2_Pcode'], 
        value_vars=['Male_Under_5', 'Female_Under_5', 'Male_5_17', 'Female_5_17'],
        var_name='Age_Group', 
        value_name='Population_Count'
    )
    
    # 6. Save the new file
    df_long.to_csv(output_file, index=False)
    
    print(f"Success! Saved filtered data to {output_file}")
    print(f"The new file has {len(df_long)} rows, each representing one age group in a county.")

if __name__ == "__main__":
    filter_school_age_data()
