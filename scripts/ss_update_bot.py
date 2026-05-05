import os
import requests
import pandas as pd
from datetime import datetime

# 1. Configuration (using GitHub Secrets)
KOBO_TOKEN = os.getenv('KOBO_TOKEN')
KOBO_FORM_ID = os.getenv('KOBO_FORM_ID')
CSV_PATH = 'data/raw/ss_raw_conflict.csv'

def fetch_kobo_data():
    print("Fetching data from KoboToolbox...")
    url = f"https://eu.kobotoolbox.org/api/v2/assets/{KOBO_FORM_ID}/data.json"
    headers = {"Authorization": f"Token {KOBO_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print(f"Error fetching Kobo data: {e}")
        return []

def update_conflict_csv(new_reports):
    if not new_reports:
        print("No new reports found in Kobo.")
        return False

    print(f"Processing {len(new_reports)} reports...")
    
    # Load existing data
    try:
        df_existing = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print("Master CSV not found. Creating a new one.")
        df_existing = pd.DataFrame()

    updates_made = False
    
    for report in new_reports:
        # Map Kobo fields to CSV columns
        # Note: These keys must match the 'Name' columns in your Kobo form
        new_row = {
            'Date': report.get('Date_of_Incident', datetime.now().strftime('%Y-%m-%d')),
            'Country': 'South Sudan',
            'Country ISO': 'SSD',
            'Admin 1': report.get('State_Admin_1', 'Unknown'),
            'Location of event': report.get('Location_of_event', 'No Information'),
            'Reported Perpetrator': report.get('Reported_Perpetrator', 'Unknown'),
            'Type of education facility': report.get('Type_of_Facility', 'Unknown'),
            'Educators Killed': report.get('Educators_Killed', 0),
            'Students Killed': report.get('Students_Killed', 0),
            'SiND Event ID': report.get('_id', 'KoboReport'), # Use Kobo ID as unique ref
            'Date Event Entered': report.get('_submission_time', '')
        }

        # Simple duplicate check: If the specific Kobo ID is already in the CSV, skip it
        if 'SiND Event ID' in df_existing.columns and str(new_row['SiND Event ID']) in df_existing['SiND Event ID'].astype(str).values:
            continue
        
        # Append new row
        df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
        updates_made = True

    if updates_made:
        df_existing.to_csv(CSV_PATH, index=False)
        print("Successfully updated master CSV with new field reports.")
        return True
    else:
        print("All reports were already in the database.")
        return False

if __name__ == "__main__":
    if not KOBO_TOKEN or not KOBO_FORM_ID:
        print("Missing Kobo credentials. Skipping field update.")
    else:
        reports = fetch_kobo_data()
        update_conflict_csv(reports)
