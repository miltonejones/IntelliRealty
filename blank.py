import streamlit as st
import pandas as pd
import json
from geocode import construct_folium_map, get_lat_lon_from_address
from util import truncate_string 
import os
from streamlit_folium import st_folium


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
 
def edit_form(filename):  

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

  # Save json_data on form submit
  if st.button("Save"):
    json_data["title"] = title
    json_data["url"] = url
    with open(json_file, 'w') as f:
      json.dump(json_data, f, indent=4)
        
    st.success("Saved!")

# st.session_state.pdf_file
def blank_page(): 
  try:
    obj = json.loads(st.session_state.selected_desc) 
    info = get_lat_lon_from_address(obj["address"] + " " + obj["city"] + ", NL")
    

    
    # selected_city = st.radio('City:',
    #                          ['Amsterdam', 'Atlanta'],
    #                          key="mode",
    #                          horizontal=True)


    # tab1, tab2 = st.tabs([f':page_facing_up: {truncate_string(obj["address"])}', f"All {st.session_state.city} listings" ])

    st.write(obj["address"])
    # with tab1: 
    col1, col2 = st.columns(2)
    with col1: 
      construct_folium_map(info["lat"], info["lon"], st.session_state.city)

    with col2:  
      viewTab, editTab = st.tabs(['View', 'Edit'])

      with viewTab:
        # st.write(obj["address"])
        st.info(f"""
{obj["description"]}

_{obj["bedroomCount"]} bedrooms, {obj["sizeInMeters"]}m2_

> Rent: {obj["rentalDetails"]["rentPrice"]}

> Deposit: {obj["rentalDetails"]["securityDeposit"]}

""") 
        st.markdown(f'[Open Listing]({obj["url"]})')
        if st.button('Remove Listing'):
          delete_pdf_and_json_files(st.session_state.pdf_file)
        

      with editTab: 
        edit_form(st.session_state.pdf_file) 

    # with tab2:  
    #   construct_folium_map(info["lat"], info["lon"], st.session_state.city) 



  except Exception as e:
      st.warning('Could not get coordinates.')
      print('Error:', e)
 