import streamlit as st
import json
import os
from datetime import datetime

# Function to read JSON data from file
def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return {}

# Function to write JSON data to file
def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to add a note to the JSON data
def add_note(data, note_text):
    note_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_note = {"date": note_date, "text": note_text}
    if 'notes' in data:
        data['notes'].append(new_note)
    else:
        data['notes'] = [new_note]

# Main function
def listing_notes(filename): 

    basename = os.path.splitext(os.path.basename(filename))[0]
    # Define the paths to the PDF and JSON files based on the filename 
    json_file_path = os.path.join('json', basename + '.json')

    # Read the JSON data from the file
    data = read_json(json_file_path)

    # Display existing notes
    if 'notes' in data:
        st.caption("Comments:")
        for note in data['notes']:
            st.markdown(f"_{note['date']}_ {note['text']}")

    if 'new_note' not in st.session_state:
        st.session_state.new_note = ''

    # Text box to enter a new note
    new_note = st.text_input("Comment:", st.session_state.new_note)

    # Button to add the note
    if st.button("Save comment"):  
        if new_note:
            add_note(data, new_note)
            write_json(data, json_file_path)
            st.success("Note added successfully!")
            st.session_state.new_note = ''
            # st.experimental_rerun()
 

 