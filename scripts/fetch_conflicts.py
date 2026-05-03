import requests
import json
import os
from datetime import datetime

def fetch_conflicts():
    # Using GDELT DOC API to find news articles about conflicts in South Sudan
    # mode=ArtList returns article metadata
    # maxrows=50 for a good sample
    # timespan=24h for real-time (last 24 hours)
    url = 'https://api.gdeltproject.org/api/v2/doc/doc?query=South%20Sudan%20(threaten%20OR%20conflict%20OR%20violence%20OR%20protest)&mode=ArtList&maxrows=50&format=JSON&timespan=24h'
    
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
