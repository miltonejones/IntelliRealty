import requests
import os  
import json
import pandas as pd
 
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

# # Replace "YOUR_GOOGLE_MAPS_API_KEY" with your actual API key
# api_key = "YOUR_GOOGLE_MAPS_API_KEY"
# address_to_search = "1600 Amphitheatre Parkway, Mountain View, CA"

# result = get_latitude_longitude(api_key, address_to_search)
# if result:
#     latitude, longitude = result
#     print(f"Latitude: {latitude}, Longitude: {longitude}")
# else:
#     print("Could not retrieve latitude and longitude.")





# def get_lat_lon_from_address(address):
#     url = f"https://nominatim.openstreetmap.org/search/{address}?format=json"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         if data:
#             return {
#                 "address": address,
#                 "lat": float(data[0]['lat']),
#                 "lon": float(data[0]['lon'])
#             }
#         else:
#             print(f"No results found for address: {address}")
#             return None
#     else:
#         print(f"Failed to fetch data for address: {address}")
#         return None

# # Example usage
# if __name__ == "__main__":
#     original_object = {
#         "name": "Sample Location",
#         "address": "1600 Amphitheatre Parkway, Mountain View, CA"
#     }

#     address = original_object["address"]
#     result = get_lat_lon_from_address(address)

#     if result:
#         original_object["lat"] = result["lat"]
#         original_object["lon"] = result["lon"]
#         print("Updated object:")
#         print(original_object)
