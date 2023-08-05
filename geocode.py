import requests
import os  
import json
import pandas as pd
import folium
from stations import get_marta_stations
from streamlit_folium import st_folium
from folium import Map, PolyLine

def add_stations_to_map(stations, map):
  for line_color, station_info in stations.items():
    coordinates = [] 
    for name, coords in station_info.items():
      coordinates.append((float(coords['lat']), float(coords['long'])))
    
    # print (coordinates)

    polyline1 = PolyLine(locations=coordinates, weight=6, color='gray')
    polyline2 = PolyLine(locations=coordinates, weight=4, color=line_color)

    polyline1.add_to(map)
    polyline2.add_to(map)

    for name, coords in station_info.items():

        folium.CircleMarker(
            location=[coords['lat'], coords['long']],
            radius=6,
            color=line_color,
            fill=True,
            popup=f'{name} Station',
            tooltip=f'{name} Station'
        ).add_to(map)



def construct_folium_map(selected_lat, selected_lon, town=None, height=400, zoom_start=12):
    folder_path = "./json"

    map = folium.Map(location=[selected_lat, selected_lon], zoom_start=zoom_start)
    
    # Create a heart-shaped icon
    heart_icon = folium.Icon(icon='heart', prefix='fa', color='red')

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                json_data = json.load(file)

            lat = json_data["lat"]
            lon = json_data["lon"]
            city = json_data["city"]
            favorite = json_data.get('favorite', False)
           
            color = "red" if favorite else "blue" 

            if town == city:   
                if selected_lat == lat:
                    folium.Marker([lat,lon],  
                                  popup=json_data.get('address', 'unknown'),
                                  tooltip=json_data.get('address', 'unknown'),
                                  icon=folium.Icon(color='orange'), 
                                  ).add_to(map) 
                elif favorite:
                    folium.Marker([lat,lon],  
                                  popup=json_data.get('address', 'unknown'),
                                  tooltip=json_data.get('address', 'unknown'),
                                  icon=folium.Icon(icon='heart', color='red'), 
                                  ).add_to(map)  
                else:
                    folium.CircleMarker(
                        location=[lat,lon],
                        radius=8,
                        popup=filename,
                        tooltip=json_data.get('address', 'unknown'),
                        color=color,
                        fill=True,
                        fill_color="#3186cc",
                    ).add_to(map)


    maps = {
      'Atlanta': 'marta_stations_geo.json',
      'Amsterdam': 'metro_stations_geo.json',
      'Rotterdam': 'rotterdam_stations_geo.json',
    }

    # station_map = "marta_stations_geo.json" if town == 'Atlanta' else "metro_stations_geo.json"
    station_map = maps[town] # 'rotterdam_stations_geo.json'
    with open(station_map, 'r') as f:
      data = json.load(f)
 
    add_stations_to_map(data, map)

    st_folium(map, width='100%', height=height) 
 
     


def get_lat_lon_from_address(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": os.getenv("GOOGLE_API_KEY") 
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return {
                "address": address,
                "lat": latitude,
                "lon": longitude
            }
        
        else:
            print(f"Error: {data['status']}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
 


print(get_lat_lon_from_address("3145 GM Maassluis, Netherlands"))

# with open('metro_stations.json', 'r') as f:
#   data = json.load(f)

# for line in data:
#   for station in data[line]:
#     address = data[line][station]
#     coords = get_lat_lon_from_address(address)
#     print ('coords', coords)
#     data[line][station] = coords

# with open('metro_stations_geo.json', 'w') as f:
#   json.dump(data, f, indent=2)

  