import streamlit as st
import pandas as pd
import json
import os
from geocode import construct_folium_map, get_lat_lon_from_address
from util import truncate_string, load_description
from notes import listing_notes, read_json, write_json
from streamlit_folium import st_folium

def get_json_filename():
  filename = st.session_state.pdf_file
  basename = os.path.splitext(os.path.basename(filename))[0] 
  return os.path.join('json', basename + '.json')

def favorite_button():
  json_path = get_json_filename()
  data = read_json(json_path)
 
  if "favorite" not in data:
    data["favorite"] = False

  if data["favorite"]:
    btn_text = "❤️ Remove from Favorites"
  else:
    btn_text = "🖤 Add to Favorites"
    
  if st.button(btn_text):
    data["favorite"] = not data["favorite"] 
    print(data)
    write_json(data, json_path)
    st.experimental_rerun()
    if data["favorite"]:
      st.success("Added to Favorites ⭐")
    else:
      st.success("Removed from Favorites ⭐")

    # 

def delete_pdf_and_json_files(filename):
  basename = os.path.splitext(os.path.basename(filename))[0]
  # Define the paths to the PDF and JSON files based on the filename
  pdf_file_path = os.path.join('src', basename + '.pdf')
  json_file_path = os.path.join('json', basename + '.json')

  # Check if the PDF and JSON files exist before deleting
  if os.path.exists(pdf_file_path):
      os.remove(pdf_file_path)
      print(f"Deleted PDF file: {pdf_file_path}")
  else:
      print(f"PDF file not found: {pdf_file_path}")

  if os.path.exists(json_file_path):
      os.remove(json_file_path)
      print(f"Deleted JSON file: {json_file_path}")
  else:
      print(f"JSON file not found: {json_file_path}")

  st.experimental_rerun()
 

def property_edit_form(filename):  
  basename = os.path.splitext(os.path.basename(filename))[0]
  # Define the paths to the PDF and JSON files based on the filename 
  json_file = os.path.join('json', basename + '.json')

  # Load JSON
  with open(json_file) as f:
    json_data = json.load(f)

  # Create form  
  st.markdown("**Edit Apartment Listing**")
  title = st.text_input("Title", json_data["title"])
  url = st.text_input("URL", json_data["url"]) 
  description = st.text_area("Description", json_data["description"])
  bedrooms = st.text_input("Bedrooms",  json_data["bedroomCount"])  
  size = st.text_input("Size (sqm)", json_data["size"])


  # Save json_data on form submit
  if st.button("Save"):

    json_data["title"] = title 
    json_data["url"] = url
    json_data["description"] = description 
    json_data["bedroomCount"] = bedrooms
    json_data["size"] = size

    with open(json_file, 'w') as f:
      json.dump(json_data, f, indent=4)
        
    st.success("Saved!")

 
 
def create_table(data):
    if 'rentalDetails' in data and 'rentOptions' in data['rentalDetails']:
        rent_options = data['rentalDetails']['rentOptions']
        if rent_options:
            table = "| Size | Beds | Baths | Price |\n|-|-|-|-|\n" 
            for option in rent_options:
                table += f"| {option['size']} sqft | {option['bedroomCount']} | {option['bathroomCount']} | {option['price']} |\n"
            table += "\n_View listing for more details_"
            return table
        else:
            return "No floorplans available"
    else:
        return "No floorplans available"
 

def property_view_panel():
  obj = json.loads(st.session_state.selected_desc) 
  st.info(f"""
    {obj["description"]}
 

    > Rent: {obj["rentalDetails"]["rentPrice"]}

    > Deposit: {obj["rentalDetails"]["securityDeposit"]}

    """) 
  
  st.markdown(f'↗️ [Open Listing]({obj["url"]})')


  with st.expander("Floor plans"):
    st.markdown(create_table(obj))


 

    

def blank_page(): 
  try:
    obj = json.loads(st.session_state.selected_desc) 
    info = get_lat_lon_from_address(obj["address"] + " " + obj["city"] ) 
 
    col1, col2 = st.columns(2)

    with col2:  
      st.write(obj["address"])
      construct_folium_map(info["lat"], info["lon"], st.session_state.city)
      favorite_button()

    with col1: 
      viewTab, editTab = st.tabs(['🏘️ Listing Details', '📝 Edit Listing'])

      with viewTab: 
        property_view_panel() 

        with st.expander("More"): 
          listing_notes(st.session_state.pdf_file) 
          if st.button('Remove Listing'):
            delete_pdf_and_json_files(st.session_state.pdf_file)

      with editTab: 
        property_edit_form(st.session_state.pdf_file)  

  except Exception as e:
      st.warning('Could not get coordinates.')
      print('Error:', e)
 