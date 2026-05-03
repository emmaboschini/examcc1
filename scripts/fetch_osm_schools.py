import requests
import json
import os

def fetch_schools_south_sudan():
    """
    Queries the Overpass API for all features tagged as 'amenity=school' 
    within the geographic boundaries of South Sudan.
    """
    print("Preparing to fetch school data from OpenStreetMap...")
    
    # Overpass API endpoint
    url = "https://overpass-api.de/api/interpreter"
    
    # Overpass Query Language (QL) script
    # We use the ISO code for South Sudan (SS) to find the area accurately
    query = """
    [out:json][timeout:60];
    area["ISO3166-1"="SS"]->.searchArea;
    (
      node["amenity"="school"](area.searchArea);
      way["amenity"="school"](area.searchArea);
      relation["amenity"="school"](area.searchArea);
    );
    out center;
    """
    
    headers = {
        "User-Agent": "SouthSudanSchoolAnalysis/1.0 (educational research)"
    }
    
    try:
        response = requests.post(url, data={'data': query}, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Convert Overpass JSON to GeoJSON format
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        for element in data.get('elements', []):
            # Determine coordinates (nodes have lat/lon, ways/relations have 'center')
            lat = element.get('lat') or element.get('center', {}).get('lat')
            lon = element.get('lon') or element.get('center', {}).get('lon')
            
            if lat and lon:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": element.get('tags', {})
                }
                # Add OSM ID for reference
                feature["properties"]["osm_id"] = element.get('id')
                geojson["features"].append(feature)
        
        output_file = os.path.join("data", "processed", "south_sudan_schools.geojson")
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2)
            
        print(f"Success! Found {len(geojson['features'])} schools.")
        print(f"Data saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_schools_south_sudan()
