import requests
import os  
import json
import pandas as pd
import folium
from streamlit_folium import st_folium


def construct_folium_map(selected_lat, selected_lon, town=None):
    folder_path = "./json"
   
  
    map = folium.Map(location=[selected_lat, selected_lon], zoom_start=12)

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                json_data = json.load(file)

            lat = json_data["lat"]
            lon = json_data["lon"]
            city = json_data["city"]
           
            color = "red" if selected_lat == lat else "blue" 

            if town == city:   
                if selected_lat == lat:
                    folium.Marker([lat,lon],  
                                  popup=json_data["address"],
                                  tooltip=json_data["address"],
                                  icon=folium.Icon(color=color), 
                                  ).add_to(map) 
                else:
                    folium.CircleMarker(
                        location=[lat,lon],
                        radius=8,
                        popup=filename,
                        tooltip=json_data["address"],
                        color="#3186cc",
                        fill=True,
                        fill_color="#3186cc",
                    ).add_to(map)


    st_folium(map, width='100%', height=400) 
 
     


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
 