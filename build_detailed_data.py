import requests
import zipfile
import io
import csv
import json
import random
from datetime import datetime, timedelta

# Expanded Bounding box to include more of Jonglei and Central Equatoria
LAT_MIN, LAT_MAX = 3.5, 9.5
LNG_MIN, LNG_MAX = 29.0, 34.5

CAMEO_CODES = {
    "180": "Assault", "181": "Abduction", "182": "Physical Assault", "183": "Sexual Violence",
    "190": "Fight/Clash", "191": "Firefight", "192": "Bombing/Explosion", "193": "Armed Fight",
    "194": "Air Strike", "195": "Small Arms Fire", "200": "Warfare", "145": "Violent Protest",
    "112": "Accusation", "130": "Threaten", "170": "Coerce", "175": "Arrest/Detain",
    "100": "Demand", "105": "Military Demand", "174": "Expulsion/Banning", "141": "Protest"
}

def get_slot_url(timestamp):
    return f"http://data.gdeltproject.org/gdeltv2/{timestamp}.export.CSV.zip"

def generate_detailed_dataset():
    now = datetime.utcnow()
    all_events = []
    
    # Sample last 7 days + 5 random days from past year
    days = [(now - timedelta(days=i)).strftime("%Y%m%d") for i in range(7)]
    days += [(now - timedelta(days=random.randint(8, 365))).strftime("%Y%m%d") for _ in range(5)]
    
    print(f"Sampling {len(days)} days...")
    
    for day in days:
        # Check all 96 slots for the most recent days, 4 for older
        num_slots = 96 if day == now.strftime("%Y%m%d") else 8
        
        for i in range(num_slots):
            ts = (datetime.strptime(day, "%Y%m%d") + timedelta(minutes=i*15)).strftime("%Y%m%d%H%M%S")
            url = get_slot_url(ts)
            try:
                r = requests.get(url, timeout=3)
                if r.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                        with z.open(z.namelist()[0]) as f:
                            reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')
                            for row in reader:
                                if len(row) < 58: continue
                                country_code, geo_name = row[53], row[52]
                                if country_code == 'OD' or 'South Sudan' in geo_name:
                                    event_code = row[26]
                                    try:
                                        lat, lng = float(row[56]), float(row[57])
                                        if LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX:
                                            # Filter for 'Conflict' or 'Protest' or 'Violence'
                                            code_int = int(event_code)
                                            if code_int >= 100 or event_code.startswith(('08','09','14')):
                                                all_events.append({
                                                    'lat': lat, 'lng': lng,
                                                    'type': CAMEO_CODES.get(event_code, f"Security Event ({event_code})"),
                                                    'date': row[1],
                                                    'source': row[60] if len(row) > 60 else "News Link",
                                                    'location': geo_name
                                                })
                                    except: continue
            except: continue
        print(f"Day {day} processed. Cumulative events: {len(all_events)}")
        
    # Jitter and de-duplicate slightly
    unique_events = []
    seen = set()
    for e in all_events:
        key = (e['lat'], e['lng'], e['type'], e['date'])
        if key not in seen:
            e['lat'] += random.uniform(-0.02, 0.02)
            e['lng'] += random.uniform(-0.02, 0.02)
            unique_events.append(e)
            seen.add(key)
            
    print(f"Total unique events found: {len(unique_events)}")
    with open('events_detailed.json', 'w') as out:
        json.dump(unique_events, out)

if __name__ == "__main__":
    generate_detailed_dataset()
