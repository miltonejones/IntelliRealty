import requests
import os  
import json
import pandas as pd
import folium
from streamlit_folium import st_folium


def construct_folium_map(selected_lat, selected_lon, town=None):
    folder_path = "./json"

    if town == 'Atlanta':
        location=[33.7552, -84.3915]
    else:
        location=[52.3731081,4.8932945]

    print(location)

    map = folium.Map(location=location, zoom_start=12)

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                json_data = json.load(file)

            lat = json_data["lat"]
            lon = json_data["lon"]
            city = json_data["city"]
            print(lat,lon)
            
            color = "red" if selected_lat == lat else "blue"

            if town == city:   
                folium.Marker([lat,lon], 
                              popup=json_data["address"],
                              icon=folium.Icon(color=color)
                              ).add_to(map) 

    st_folium(map, width='100%', height=500) 

def construct_folium_singleton_map(selected_lat, selected_lon, town=None): 

    if town == 'Atlanta':
        location=[33.7552, -84.3915]
    else:
        location=[52.3731081,4.8932945]
 

    map = folium.Map(location=location, zoom_start=12)

    folium.Marker([selected_lat,selected_lon]).add_to(map)
                
    st_folium(map, width='100%', height=500) 

    
 
def construct_dataframe_with_selected(selected_lat, selected_lon, town=None): 
    folder_path = "./json"
    data = {
        "latitude": [],
        "longitude": [],
        "size": [],
        "color": []
    }

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                json_data = json.load(file)

            lat = json_data["lat"]
            lon = json_data["lon"]
            city = json_data["city"]

            if town == city: 
                data["latitude"].append(lat)
                data["longitude"].append(lon)

                if lat == selected_lat and lon == selected_lon:
                    data["size"].append(120)
                    data["color"].append("#00FF00")
                else:
                    data["size"].append(10)
                    data["color"].append("#0000FF")

    df = pd.DataFrame(data)
    # print("df!", data)
    return df
 
 


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
 