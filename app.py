from dotenv import load_dotenv
import os 
# import json
# from geocode import get_lat_lon_from_address
from langchain.chains import ConversationalRetrievalChain 
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from blank import blank_page
from util import get_document_list, displayPDF, truncate_string, initialize_session, load_source_documents, load_description, load_source_document, save_uploaded_file
import streamlit as st

load_dotenv()
  
# Load the OpenAI API key from the environment variable
if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
  print("OPENAI_API_KEY is not set")
  exit(1) 
   

 

# build and render page sidebar 
def render_sidebar():
  
  with st.sidebar:

    if st.button("🏡 **IntelliRealty**",  help="Reset conversation"):
      st.session_state.chat_history = [] 
    
    selected_city = st.selectbox('City:',
                             ['Amsterdam', 'Atlanta'],
                             key="city") 
    
    source_docs = get_document_list(st.session_state.city) 

    st.session_state.source_docs = source_docs 

    # Display radio buttons and handle document selection
    selected_option = st.radio('Listing:', 
                                list(source_docs.keys()), 
                                key="selected_option_key", 
                                format_func=truncate_string,
                                index=0)
 
    # Update session variable on button selection
    if selected_option:
      st.session_state.pdf_file = source_docs[selected_option]["path"]
      st.session_state.selected_option = selected_option  

    with st.expander(":gear: Settings"):
      # Create the slider and update 'llm_temparature' when it's changed
      st.session_state.llm_temparature = st.slider('Set LLM temperature', 0.0, 1.0, step=0.1, value=st.session_state.llm_temparature )
   

    with st.expander(":file_folder: Add listing"):
      uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

      if uploaded_files is not None:
        for uploaded_file in uploaded_files:
          # Save each uploaded file and display a success message
          file_path = save_uploaded_file(uploaded_file)
          st.success(f"File saved successfully: {file_path}")   

 
def main(): 

  st.set_page_config(page_title="IntelliRealty", layout="wide") 
  
  # set initial session values
  initialize_session() 

  # draw page side bar
  render_sidebar()
 
  # Create a ChatOpenAI object for streaming chat with specified temperature
  chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()],  model="gpt-3.5-turbo", max_tokens=1024, temperature=st.session_state.llm_temparature)

  # Load the source document for the conversation retrieval
  db = load_source_document(st.session_state.pdf_file)

  # db = load_source_documents(st.session_state.city)

  # Create a conversation chain that uses the vectordb as a retriever, allowing for chat history management
  qa = ConversationalRetrievalChain.from_llm(chat, db.as_retriever())

  # Load the description using the conversation chain and store the answer in selected_desc
  loc = load_description(qa, st.session_state.pdf_file)['answer'] 

  st.session_state.selected_desc = loc 

  # render existing chats
  for message in st.session_state.chat_history:
    with st.chat_message("user"):
      st.markdown(message[0])
    with st.chat_message("assistant"):
      st.markdown(message[1])
          
  # React to user input
  if prompt := st.chat_input(f"Ask me anything about '{st.session_state.selected_option}'"):

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Display a spinner while generating the answer
    with st.spinner(text="Generating answer..."):
      # Use the conversation chain (qa) to generate an answer based on the prompt and chat history
      result = qa({"question": prompt, "chat_history": st.session_state.chat_history})

      # Get the answer from the result
      response = f"{result['answer']}"

      # Append the prompt and response to the chat history
      st.session_state.chat_history.append((prompt, response))

      # Display the assistant's response in the chat message container
      with st.chat_message("assistant"):
          st.markdown(response)

  # empty chat screen
  else:  
    if len(st.session_state.chat_history) == 0:
      blank_page()
      if st.button('Refresh Listing'):
          load_description(qa, st.session_state.pdf_file, True) 
       

if __name__ == "__main__":
  main()
