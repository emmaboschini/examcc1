import requests
import zipfile
import io
import csv
import json
from datetime import datetime, timedelta

def get_slot_url(timestamp):
    return f"http://data.gdeltproject.org/gdeltv2/{timestamp}.export.CSV.zip"

import time
from datetime import datetime, timedelta

def update_data():
    now = datetime.utcnow()
    now = now.replace(minute=(now.minute // 15) * 15, second=0, microsecond=0)
    
    # Bounding box for Juba and Bor areas
    LAT_MIN, LAT_MAX = 4.5, 6.5
    LNG_MIN, LNG_MAX = 30.5, 32.5
    
    events = []
    slots_checked = 0
    slots_found = 0
    
    # We only need the last few hours for an automated "hourly" feel
    for i in range(12): # Last 3 hours
        timestamp = (now - timedelta(minutes=i*15)).strftime("%Y%m%d%H%M%S")
        url = get_slot_url(timestamp)
        slots_checked += 1
        
        try:
            r_zip = requests.get(url, timeout=5)
            if r_zip.status_code == 200:
                slots_found += 1
                with zipfile.ZipFile(io.BytesIO(r_zip.content)) as z:
                    csv_filename = z.namelist()[0]
                    with z.open(csv_filename) as f:
                        reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')
                        for row in reader:
                            if len(row) < 61: continue
                            event_code, country_code = row[26], row[37]
                            lat_str, lng_str, source_url = row[56], row[57], row[60]
                            
                            if country_code == 'OD':
                                try:
                                    lat = float(lat_str) if lat_str else None
                                    lng = float(lng_str) if lng_str else None
                                    
                                    # Spatial filter: Juba & Bor focus
                                    if lat and lng and LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX:
                                        code_val = int(event_code)
                                        if code_val >= 100:
                                            category = "Conflict"
                                            if 180 <= code_val <= 189: category = "Assault/Violence"
                                            elif 190 <= code_val <= 199: category = "Fight/Clash"
                                            
                                            events.append({
                                                'lat': lat,
                                                'lng': lng,
                                                'category': category,
                                                'date': row[1],
                                                'source': source_url,
                                                'location': row[52]
                                            })
                                except (ValueError, TypeError):
                                    continue
        except Exception:
            continue
            
    print(f"Checked {slots_checked} slots. Found {len(events)} events in the Juba-Bor corridor.")
    with open('realtime_events.json', 'w') as out:
        json.dump(events, out)

if __name__ == "__main__":
    while True:
        print(f"[{datetime.now()}] Starting hourly update...")
        update_data()
        print("Update complete. Sleeping for 60 minutes...")
        time.sleep(3600)
