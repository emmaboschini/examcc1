import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration
KOBO_TOKEN = os.getenv('KOBO_TOKEN')
KOBO_FORM_ID = os.getenv('KOBO_FORM_ID')
CSV_PATH = 'data/raw/ss_raw_conflict.csv'

# ReliefWeb Configuration
# We search for the last 30 days of education-related incidents in South Sudan
RW_URL = "https://api.reliefweb.int/v2/reports"
RW_PARAMS = {
    "appname": "SouthSudanEducationRiskDashboard",
    "filter[field]": "primary_country.name",
    "filter[value]": "South Sudan",
    "query[value]": "(school OR education OR teacher OR student) AND (attack OR armed OR shooting OR bombing OR looted)",
    "sort[]": "date:desc",
    "limit": 10
}

def fetch_kobo_data():
    if not KOBO_TOKEN or not KOBO_FORM_ID:
        print("Missing Kobo credentials. Skipping field update.")
        return []
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

def fetch_reliefweb_news():
    print("Fetching news from ReliefWeb...")
    # Use a completely standard User-Agent to avoid being flagged
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Simplified params - sometimes less is more with OCHA's API
    params = {
        "appname": "humanitarian-mapping-tool",
        "filter[field]": "primary_country.name",
        "filter[value]": "South Sudan",
        "query[value]": "school attack OR education attack",
        "sort[]": "date:desc",
        "limit": 5
    }
    try:
        response = requests.get(RW_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json().get('data', [])
        print(f"Successfully found {len(data)} potential news items.")
        return data
    except Exception as e:
        print(f"Error fetching ReliefWeb news: {e}")
        return []

def update_conflict_csv(kobo_reports, rw_news):
    # Load existing data
    try:
        df_existing = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        df_existing = pd.DataFrame(columns=['Date', 'Admin 1', 'Location of event', 'Reported Perpetrator', 'Type of education facility', 'Educators Killed', 'Students Killed', 'SiND Event ID', 'Status', 'Source URL'])

    if 'Status' not in df_existing.columns:
        df_existing['Status'] = 'verified'
    if 'Source URL' not in df_existing.columns:
        df_existing['Source URL'] = ''

    updates_made = False

    # Process Kobo (Mark as Verified)
    for report in kobo_reports:
        uid = str(report.get('_id', ''))
        if uid and uid not in df_existing['SiND Event ID'].astype(str).values:
            new_row = {
                'Date': report.get('Date_of_Incident', datetime.now().strftime('%Y-%m-%d')),
                'Country': 'South Sudan',
                'Admin 1': report.get('State_Admin_1', 'Unknown'),
                'Location of event': report.get('Location_of_event', 'Field Report'),
                'Reported Perpetrator': report.get('Reported_Perpetrator', 'Unknown'),
                'Type of education facility': report.get('Type_of_Facility', 'Unknown'),
                'Educators Killed': report.get('Educators_Killed', 0),
                'Students Killed': report.get('Students_Killed', 0),
                'SiND Event ID': uid,
                'Status': 'verified',
                'Source URL': ''
            }
            df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
            updates_made = True

    # Process ReliefWeb (Mark as Unverified)
    for news in rw_news:
        url = news.get('href', '')
        # Check if URL already exists
        if url and url not in df_existing['Source URL'].astype(str).values:
            fields = news.get('fields', {})
            new_row = {
                'Date': fields.get('date', {}).get('created', datetime.now().strftime('%Y-%m-%d'))[:10],
                'Country': 'South Sudan',
                'Admin 1': 'No Information', # News often doesn't specify Admin1 in the API title
                'Location of event': fields.get('title', 'News Alert'),
                'Reported Perpetrator': 'Unverified Source',
                'Type of education facility': 'School (Unconfirmed)',
                'Educators Killed': 0,
                'Students Killed': 0,
                'SiND Event ID': f"RW-{news.get('id')}",
                'Status': 'unverified',
                'Source URL': url
            }
            df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
            updates_made = True

    if updates_made:
        df_existing.to_csv(CSV_PATH, index=False)
        print("Database updated successfully.")
    else:
        print("No new data to add.")

if __name__ == "__main__":
    kobo = fetch_kobo_data()
    # ReliefWeb is temporarily on hold
    rw = [] 
    update_conflict_csv(kobo, rw)
