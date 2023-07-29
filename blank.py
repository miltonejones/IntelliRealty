import streamlit as st
import pandas as pd
import json
from geocode import get_lat_lon_from_address, construct_dataframe_with_selected
from util import truncate_string 
import os


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
 


def blank_page(): 
  try:
    obj = json.loads(st.session_state.selected_desc) 
    info = get_lat_lon_from_address(obj["address"] + " " + obj["city"] + ", NL")
    # print('geocode', info)

    # st.caption(st.session_state.selected_desc)


    dots = construct_dataframe_with_selected(info["lat"], info["lon"], st.session_state.city)
    
    # print('map', dots)

    ## Create a sample DataFrame with latitude and longitude values
    data = pd.DataFrame({
        'latitude': [info["lat"]],
        'longitude': [info["lon"]],
        'size': 50,
        'color': '#ff0000'
    })


    tab1, tab2 = st.tabs([f':page_facing_up: **{obj["address"]}**', f"All {st.session_state.city} listings" ])

    with tab2: 
      st.map(dots)

    with tab1: 
      col1, col2 = st.columns(2)
      with col1:
        st.map(data)
      with col2:  
        st.write(obj["address"])
        st.info(f"""
{obj["description"]}

_{obj["bedroomCount"]} bedrooms, {obj["sizeInMeters"]}m2_

> Rent: {obj["rentalDetails"]["rentPrice"]}

> Deposit: {obj["rentalDetails"]["securityDeposit"]}

""") 
        st.markdown(f'[Open Listing]({obj["url"]})')
        if st.button('Remove Listing'):
          confirmation = st.radio("Are you sure you want to delete this document?", ("No", "Yes"), index=0)
          if confirmation == "Yes":
            delete_pdf_and_json_files(st.session_state.pdf_file)
          




  except Exception as e:
      st.warning('Could not get coordinates.')
      print('Error:', e)
 