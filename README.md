# IntelliRealty Assistant

This is a real estate assistant app built with Streamlit and LangChain. It allows users to:

- Browse and select real estate listings
- View listing details and descriptions 
- Interact through conversational question answering
- Adjust the chatbot temperature
- Upload new listings

## Features

- Listing browser with radio button selection
- Interactive map view (not implemented yet)
- Conversational QA chatbot powered by LangChain and GPT-3.5 Turbo 
- Streamlit sidebar for navigation and settings
- Ability to set the chatbot temperature 
- File uploader to add new listings

## Setup

### Prerequisites

- Python 3.7+
- Streamlit 
- LangChain
- OpenAI API key

### Installation

1. Clone this repo
2. Copy `.env.example` to `.env` and add your OpenAI key 
3. Install requirements: `pip install -r requirements.txt`
4. Run the app: `streamlit run app.py`

Here are the main interactive components in the real estate assistant app and what they do:

**Sidebar Buttons**

- 🏡 **IntelliRealty**: Resets the conversation history

- View radio buttons: Switch between Listing and Map views

- City radio buttons: Filter listings by city

**Sidebar Selectboxes** 

- Property: Select listing PDF to load details and chat about

- Add to Favorites: Toggle favorite status of a listing

**Main Page Buttons**

- Chat input box: Enter a question to ask the assistant

- Refresh Listing: Reload the listing details 

- Remove Listing: Delete the PDF, JSON, and index for listing

- Save (in Edit tab): Save edited listing details to JSON 

**Main Page Interactive**

- Floor plan expander: Show floor plans table

- More expander: Show listing notes

- Edit tab form: Edit listing details like title, beds, etc. 



Here are some more details about the functions in the real estate assistant app interface:

- `render_sidebar()`: This draws the left sidebar with navigation options like selecting a city, listing, and chatbot settings. It handles setting up the session state variables.

- `main()`: The main function that brings together all the components. It initializes the session, renders the sidebar, sets up the chatbot, loads the listing documents, and handles the chat UI.

- `get_document_list()`: Loads the PDF listing files from the `src` folder and creates a dictionary mapping clean names to file paths. It optionally filters by city.

- `load_source_documents()`: Creates a FAISS document store from the PDF listing files to power retrieval.

- `load_description()`: Uses the conversation chain to generate a property description in JSON format for a given listing PDF. Caches the result to avoid re-generating each time.

- `load_source_document()`: Loads a single PDF into a FAISS document store for faster chat retrieval.

- `save_uploaded_file()`: Handles saving a new uploaded PDF to the `src` folder and processing it.

- `initialize_session()`: Sets up initial state for streamlit session variables.

- `truncate_string()`: Trims long listing names for the sidebar selection UI.

- `blank_page()`: Renders the main content area. Has tabs for property details and editing. Displays the map.

- `property_view_panel()`: Shows the listing details and description.

- `create_table()`: Generates a Markdown table from the floor plan data.

- `property_edit_form()`: Allows editing the listing data. Saves back to the JSON file.

- `delete_pdf_and_json_files()`: Deletes the PDF, JSON, and FAISS index for a listing.
 

## License

This project is open source and available under the MIT License.