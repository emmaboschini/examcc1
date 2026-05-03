import requests
import json

def fetch_schools():
    # 1. The "Query": We are telling the Overpass API exactly what we want.
    # [out:json] -> Give us the result in JSON format.
    # area["name"="South Sudan"] -> Look inside the borders of South Sudan.
    # nwr["amenity"="school"](area.searchArea) -> Find all Nodes, Ways, and Relations tagged as a school.
    overpass_query = """
    [out:json][timeout:90];
    area(3601656678)->.searchArea;
    (
      nwr["amenity"="school"](area.searchArea);
    );
    out center;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    headers = {
        'User-Agent': 'GeminiCLIMapBot/1.0 (Educational Project; contact: example@example.com)'
    }
    
    print("Connecting to OpenStreetMap (Overpass API)... This may take a moment.")
    response = requests.post(url, data={'data': overpass_query}, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Could not connect to API (Status {response.status_code})")
        return

    data = response.json()
    elements = data.get('elements', [])
    
    # 2. Convert to GeoJSON: Standard map format
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for element in elements:
        # Determine location (Overpass returns 'lat'/'lon' or 'center' for areas)
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
            # Clean up the name if it exists
            name = feature["properties"].get("name", "Unnamed School")
            feature["properties"]["name"] = name
            
            geojson["features"].append(feature)

    # 3. Save the file
    with open('south_sudan_schools.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)

    print(f"Success! Found {len(geojson['features'])} schools.")
    print("Saved to 'south_sudan_schools.geojson'")

if __name__ == "__main__":
    fetch_schools()
