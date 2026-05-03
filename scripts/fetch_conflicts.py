import requests
import json
import os
from datetime import datetime

def fetch_conflicts():
    # Using more aggressive keywords to find serious events with casualties or armed action
    # We look for: (South Sudan) AND (killed OR casualty OR dead OR explosion OR shooting OR gunfire OR gunmen OR "armed action" OR clashes)
    query = 'South%20Sudan%20(killed%20OR%20dead%20OR%20casualty%20OR%20casualties%20OR%20explosion%20OR%20shooting%20OR%20gunfire%20OR%20gunmen%20OR%20"armed%20action"%20OR%20clashes)'
    url = f'https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=ArtList&maxrows=50&format=JSON&timespan=24h'
    
    print(f"Fetching news-based conflict data from GDELT at {datetime.now()}...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            
            # Since DOC API doesn't provide exact Lat/Long, we'll place them in state centers 
            # or Juba as placeholders, or skip articles without specific city names.
            # For this MVP, we focus on providing a live news feed on the map.
            
            output_path = 'data/processed/realtime_conflicts.json'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'articles': articles, 'last_update': datetime.now().isoformat()}, f, indent=2)
            
            print(f"Successfully saved {len(articles)} recent articles.")
        else:
            print(f"Error: API returned status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_conflicts()
