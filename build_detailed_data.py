import requests
import zipfile
import io
import csv
import json
import random
import hashlib
import math
from datetime import datetime, timedelta

# Schools for Center points
JUBA_SCHOOL = [4.88, 31.63]
BOR_SCHOOL = [6.21, 31.55]
RADIUS_KM = 15.0

CAMEO_CODES = {
    "180": "Assault", "181": "Abduction", "182": "Physical Assault", "183": "Sexual Violence",
    "190": "Fight/Clash", "191": "Firefight", "192": "Bombing/Explosion", "193": "Armed Fight",
    "194": "Air Strike", "195": "Small Arms Fire", "200": "Warfare", "145": "Violent Protest",
    "112": "Accusation", "130": "Threaten", "170": "Coerce", "175": "Arrest/Detain",
    "100": "Demand", "105": "Military Demand", "174": "Expulsion/Banning", "141": "Protest"
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def get_slot_url(timestamp):
    return f"http://data.gdeltproject.org/gdeltv2/{timestamp}.export.CSV.zip"

def is_near_schools(lat, lng):
    dist_juba = haversine(lat, lng, JUBA_SCHOOL[0], JUBA_SCHOOL[1])
    dist_bor = haversine(lat, lng, BOR_SCHOOL[0], BOR_SCHOOL[1])
    return dist_juba <= RADIUS_KM or dist_bor <= RADIUS_KM

def generate_detailed_dataset():
    now = datetime.utcnow()
    all_events = []
    
    # Extensive sampling: last 30 days daily + 60 random days from the year
    days = [(now - timedelta(days=i)).strftime("%Y%m%d") for i in range(30)]
    days += [(now - timedelta(days=random.randint(31, 365))).strftime("%Y%m%d") for _ in range(60)]
    
    print(f"Sampling {len(set(days))} unique days for 15km radius around Juba and Bor...")
    
    unique_days = sorted(list(set(days)), reverse=True)
    
    for day in unique_days:
        # Sample more slots for recent days
        slots_to_check = ["000000", "060000", "120000", "180000"]
        if (datetime.utcnow() - datetime.strptime(day, "%Y%m%d")).days < 7:
            # Check every hour for the last week
            slots_to_check = [f"{h:02d}0000" for h in range(24)]

        for slot in slots_to_check:
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
                                    if is_near_schools(lat, lng):
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
        print(f"Processed {day}, cumulative matches: {len(all_events)}")
        
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
            
    print(f"Total stable unique events found in 15km radii: {len(unique_events)}")
    with open('events_detailed.json', 'w') as out:
        json.dump(unique_events, out)

if __name__ == "__main__":
    generate_detailed_dataset()
