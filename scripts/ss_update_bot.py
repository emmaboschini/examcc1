import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration
KOBO_TOKEN = os.getenv('KOBO_TOKEN')
KOBO_FORM_ID = os.getenv('KOBO_FORM_ID')
CSV_PATH = 'data/raw/ss_raw_conflict.csv'

def fetch_kobo_data():
    if not KOBO_TOKEN or not KOBO_FORM_ID:
        print("⚠️ Missing Kobo credentials (KOBO_TOKEN or KOBO_FORM_ID).")
        print("Please ensure these are set in your GitHub Repository Secrets.")
        return []
    
    # Ensure token format is correct
    token = KOBO_TOKEN.strip()
    if not token.startswith('Token '):
        token = f"Token {token}"
        
    # Try EU first, then Global if EU fails or if we want to be thorough
    urls = [
        f"https://eu.kobotoolbox.org/api/v2/assets/{KOBO_FORM_ID}/data.json",
        f"https://kf.kobotoolbox.org/api/v2/assets/{KOBO_FORM_ID}/data.json"
    ]
    
    for url in urls:
        print(f"Trying Kobo API: {url}...")
        headers = {"Authorization": token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # Some versions return a list directly, others use 'results'
                if isinstance(data, list):
                    results = data
                else:
                    results = data.get('results', [])
                
                print(f"✅ Success! Found {len(results)} reports at {url}")
                return results
            else:
                print(f"ℹ️ Status {response.status_code} at {url}")
        except Exception as e:
            print(f"❌ Connection error at {url}: {e}")
            
    print("❌ Could not fetch data from any Kobo server.")
    return []

def update_conflict_csv(kobo_reports):
    # Load existing data
    try:
        df_existing = pd.read_csv(CSV_PATH)
        print(f"Loaded existing database with {len(df_existing)} entries.")
    except FileNotFoundError:
        print("Starting new database.")
        df_existing = pd.DataFrame(columns=['Date', 'Country', 'Admin 1', 'Location of event', 'Reported Perpetrator', 'Type of education facility', 'Educators Killed', 'Students Killed', 'SiND Event ID', 'Status', 'Source URL'])

    if 'Status' not in df_existing.columns:
        df_existing['Status'] = 'verified'
    if 'Source URL' not in df_existing.columns:
        df_existing['Source URL'] = ''
    if 'Country' not in df_existing.columns:
        df_existing['Country'] = 'South Sudan'

    updates_made = False
    new_count = 0

    # Process Kobo (Mark as Verified)
    for report in kobo_reports:
        uid = str(report.get('_id', report.get('id', '')))
        if uid and uid not in df_existing['SiND Event ID'].astype(str).values:
            # Helper to safely get numbers
            def safe_int(val):
                try:
                    return int(float(val)) if val and str(val).strip() else 0
                except:
                    return 0

            # Clean State Name to match map logic
            state_raw = str(report.get('State_Admin_1', 'Unknown'))
            state_clean = state_raw.replace(' State', '').strip()

            new_row = {
                'Date': report.get('Date_of_Incident', datetime.now().strftime('%Y-%m-%d')),
                'Country': 'South Sudan',
                'Admin 1': state_clean,
                'Location of event': report.get('Location_of_event', 'Field Report'),
                'Reported Perpetrator': report.get('Reported_Perpetrator', 'Unknown'),
                'Type of education facility': report.get('Type_of_Facility', 'Unknown'),
                'Educators Killed': safe_int(report.get('Educators_Killed', 0)),
                'Students Killed': safe_int(report.get('Students_Killed', 0)),
                'SiND Event ID': uid,
                'Status': 'field_update',
                'Source URL': ''
            }
            df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
            updates_made = True
            new_count += 1

    if updates_made:
        # Sort so newest are at top if we want, but CSV usually appends
        df_existing.to_csv(CSV_PATH, index=False)
        print(f"🚀 Database updated with {new_count} new field reports.")
    else:
        print("ℹ️ No new field reports found in this sync.")

if __name__ == "__main__":
    kobo = fetch_kobo_data()
    update_conflict_csv(kobo)
