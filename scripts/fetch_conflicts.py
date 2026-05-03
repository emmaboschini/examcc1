import requests
import json
import os
from datetime import datetime

def fetch_conflicts():
    # Stricter keywords for high-intensity events
    # We query for (South Sudan) AND (killed OR dead OR explosion OR gunfire OR shooting)
    keywords = ["killed", "dead", "casualty", "casualties", "explosion", "shooting", "gunfire", "gunmen", "bombardment", "strike"]
    query_str = "South%20Sudan%20(" + "%20OR%20".join(keywords) + ")"
    url = f'https://api.gdeltproject.org/api/v2/doc/doc?query={query_str}&mode=ArtList&maxrows=75&format=JSON&timespan=48h'
    
    print(f"Fetching HIGH-INTENSITY conflict data from GDELT at {datetime.now()}...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            all_articles = response.json().get('articles', [])
            
            # LOCAL FILTER: Double-check each article to be 100% sure it contains a serious keyword
            # This filters out "noise" that the API might include
            strict_articles = []
            for art in all_articles:
                title_lower = art.get('title', '').lower()
                if any(kw in title_lower for kw in keywords):
                    strict_articles.append(art)
            
            output_path = 'data/processed/realtime_conflicts.json'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'articles': strict_articles, 'last_update': datetime.now().isoformat()}, f, indent=2)
            
            print(f"Success! Found {len(strict_articles)} high-intensity events after strict filtering.")
        elif response.status_code == 429:
            print("Error: Hit GDELT speed limit (429). The robot will try again in 30 minutes.")
        else:
            print(f"Error: API returned status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_conflicts()
