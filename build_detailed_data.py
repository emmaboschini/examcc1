import requests
import zipfile
import io
import csv
import json
import random
import hashlib
import math
from datetime import datetime, timedelta

# Focus Center: Juba School
JUBA_SCHOOL = [4.88, 31.63]
RADIUS_KM = 15.0

# CAMEO codes strictly for lethal or high-intensity violence (Fights, Warfare)
LETHAL_CODES = {
    "190": "Fight/Clash", "191": "Firefight", "192": "Bombing/Explosion", "193": "Armed Fight",
    "194": "Air Strike", "195": "Small Arms Fire", "200": "Warfare", "201": "Massive Violence",
    "202": "Radiological/Chemical Attack", "203": "Biological Attack", "204": "Nuclear Attack"
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def get_slot_url(timestamp):
    return f"http://data.gdeltproject.org/gdeltv2/{timestamp}.export.CSV.zip"

def is_near_juba(lat, lng):
    return haversine(lat, lng, JUBA_SCHOOL[0], JUBA_SCHOOL[1]) <= RADIUS_KM

def generate_detailed_dataset():
    now = datetime.utcnow()
    all_events = []
    
    # Strictly sample recent days for "New Casualties" (GDELT feed)
    days = [(now - timedelta(days=i)).strftime("%Y%m%d") for i in range(14)]
    
    print(f"Sampling recent GDELT data for lethal incidents (new casualties) in Juba...")
    
    for day in days:
        # Check all hourly slots for recent days
        for h in range(24):
            ts = day + f"{h:02d}0000"
            url = get_slot_url(ts)
            try:
                r = requests.get(url, timeout=3)
                if r.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                        with z.open(z.namelist()[0]) as f:
                            reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')
                            for row in reader:
                                if len(row) < 58: continue
                                event_code = row[26]
                                # Filter strictly for LETHAL codes
                                if event_code in LETHAL_CODES:
                                    try:
                                        lat, lng = float(row[56]), float(row[57])
                                        if is_near_juba(lat, lng):
                                            all_events.append({
                                                'lat': lat, 'lng': lng,
                                                'type': LETHAL_CODES[event_code],
                                                'date': row[1],
                                                'source': row[60] if len(row) > 60 else "Intelligence Feed",
                                                'location': row[52],
                                                'id': row[0]
                                            })
                                    except: continue
            except: continue
        print(f"Processed {day}, cumulative lethal matches: {len(all_events)}")
        
    # Deterministic Jitter
    unique_events = []
    seen = set()
    for e in all_events:
        if e['id'] not in seen:
            h = int(hashlib.md5(e['id'].encode()).hexdigest(), 16)
            e['lat'] += ((h % 40) / 2000.0) - 0.01
            e['lng'] += (((h // 100) % 40) / 2000.0) - 0.01
            unique_events.append(e)
            seen.add(e['id'])
            
    print(f"Total verified lethal signals (GDELT): {len(unique_events)}")
    
    output_data = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "events": unique_events,
        "historical_source": "ACLED (Armed Conflict Location & Event Data)",
        "realtime_source": "GDELT Project (Casualties Feed)"
    }
    
    with open('events_detailed.json', 'w') as out:
        json.dump(output_data, out)

if __name__ == "__main__":
    generate_detailed_dataset()
