import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration
KOBO_TOKEN = os.getenv('KOBO_TOKEN')
KOBO_FORM_ID = os.getenv('KOBO_FORM_ID')
CSV_PATH = 'data/raw/ss_kobo_entries.csv'

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
                if isinstance(data, list):
                    results = data
                else:
                    results = data.get('results', [])
                
                print(f"✅ Success! Connected to {url}")
                print(f"📊 Total records found in Kobo: {len(results)}")
                
                if len(results) > 0:
                    print("🔍 Diagnostic: Full content of the latest report:")
                    import json
                    print(json.dumps(results[0], indent=2))
                
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
            # Helper to safely get numbers
            def safe_int(val):
                try:
                    return int(float(val)) if val and str(val).strip() else 0
                except:
                    return 0

            # Map the actual Kobo field names (Flexible mapping)
            k_date = report.get('Date_of_the_Incident') or report.get('Date_of_Incident') or datetime.now().strftime('%Y-%m-%d')
            k_state = report.get('State') or report.get('State_Admin_1') or 'Unknown'
            k_location = report.get('Name_of_the_facility') or report.get('Location_of_event') or 'Field Report'
            k_facility = report.get('Type_of_Facility_yo_select_more_than_one') or report.get('Type_of_Facility') or 'Unknown'
            k_perpetrator = report.get('Reported_Perpetrator') or 'Unknown'
            
            # Clean State Name to match map logic
            state_clean = str(k_state).replace(' State', '').strip()

            new_row = {
                'Date': k_date,
                'Country': 'South Sudan',
                'Admin 1': state_clean,
                'Location of event': k_location,
                'Reported Perpetrator': k_perpetrator,
                'Type of education facility': k_facility,
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
