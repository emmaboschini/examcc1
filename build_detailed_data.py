import requests
import zipfile
import io
import csv
import json
import random
import hashlib
from datetime import datetime, timedelta

# Tightened Bounding box for Juba and Bor areas only
LAT_JUBA_MIN, LAT_JUBA_MAX = 4.7, 5.1
LNG_JUBA_MIN, LNG_JUBA_MAX = 31.4, 31.8

LAT_BOR_MIN, LAT_BOR_MAX = 6.0, 6.4
LNG_BOR_MIN, LNG_BOR_MAX = 31.4, 31.7

CAMEO_CODES = {
    "180": "Assault", "181": "Abduction", "182": "Physical Assault", "183": "Sexual Violence",
    "190": "Fight/Clash", "191": "Firefight", "192": "Bombing/Explosion", "193": "Armed Fight",
    "194": "Air Strike", "195": "Small Arms Fire", "200": "Warfare", "145": "Violent Protest",
    "112": "Accusation", "130": "Threaten", "170": "Coerce", "175": "Arrest/Detain",
    "100": "Demand", "105": "Military Demand", "174": "Expulsion/Banning", "141": "Protest"
}

def get_slot_url(timestamp):
    return f"http://data.gdeltproject.org/gdeltv2/{timestamp}.export.CSV.zip"

def is_in_target_areas(lat, lng):
    in_juba = LAT_JUBA_MIN <= lat <= LAT_JUBA_MAX and LNG_JUBA_MIN <= lng <= LNG_JUBA_MAX
    in_bor = LAT_BOR_MIN <= lat <= LAT_BOR_MAX and LNG_BOR_MIN <= lng <= LNG_BOR_MAX
    return in_juba or in_bor

def generate_detailed_dataset():
    now = datetime.utcnow()
    all_events = []
    
    # Sample last 14 days + some random samples from the year
    days = [(now - timedelta(days=i)).strftime("%Y%m%d") for i in range(14)]
    days += [(now - timedelta(days=random.randint(15, 365))).strftime("%Y%m%d") for _ in range(5)]
    
    print(f"Sampling {len(days)} days for Juba and Bor specifically...")
    
    for day in days:
        # 4 samples per day to keep it fast
        for slot in ["000000", "060000", "120000", "180000"]:
            ts = day + slot
            url = get_slot_url(ts)
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                        with z.open(z.namelist()[0]) as f:
                            reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')
                            for row in reader:
                                if len(row) < 58: continue
                                try:
                                    lat, lng = float(row[56]), float(row[57])
                                    if is_in_target_areas(lat, lng):
                                        event_code = row[26]
                                        if int(event_code) >= 100 or event_code.startswith(('08','09','14')):
                                            all_events.append({
                                                'lat': lat, 'lng': lng,
                                                'type': CAMEO_CODES.get(event_code, f"Security Event ({event_code})"),
                                                'date': row[1],
                                                'source': row[60] if len(row) > 60 else "News Link",
                                                'location': row[52],
                                                'id': row[0]
                                            })
                                except: continue
            except: continue
        print(f"Processed day {day}, cumulative matches: {len(all_events)}")
        
    # Deterministic Jitter (stays same for same Event ID)
    unique_events = []
    seen = set()
    for e in all_events:
        if e['id'] not in seen:
            # Deterministic offset based on ID
            h = int(hashlib.md5(e['id'].encode()).hexdigest(), 16)
            e['lat'] += ((h % 40) / 2000.0) - 0.01
            e['lng'] += (((h // 100) % 40) / 2000.0) - 0.01
            unique_events.append(e)
            seen.add(e['id'])
            
    print(f"Total stable unique events found: {len(unique_events)}")
    with open('events_detailed.json', 'w') as out:
        json.dump(unique_events, out)

if __name__ == "__main__":
    generate_detailed_dataset()
