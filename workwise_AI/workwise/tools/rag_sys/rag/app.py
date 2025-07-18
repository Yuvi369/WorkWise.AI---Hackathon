import streamlit as st
import os
import traceback
import json
from main import RAG
from langchain_core.messages import HumanMessage, AIMessage
from utils.common import normalize_file_paths

# Set page configuration
st.set_page_config(page_title="Talk with your Document", layout="wide")

# Initialize RAG class
@st.cache_resource
def init_rag():
    return RAG()

# Initialize RAG instance
try:
    rag = init_rag()
except Exception as e:
    st.error(f"Failed to initialize RAG: {str(e)}")
    st.write(traceback.format_exc())

use_cache = rag.config["app"].get("use_cache", False)

# File upload for adding or deleting PDFs
st.sidebar.header("Manage PDF Documents")
uploaded_files = st.sidebar.file_uploader("Upload new PDF files", type="pdf", accept_multiple_files=True)
delete_files = st.sidebar.file_uploader("Select PDFs to delete", type="pdf", accept_multiple_files=True)

# Process uploaded files
if uploaded_files or delete_files:
    temp_dir = "temp_pdfs"
    os.makedirs(temp_dir, exist_ok=True)
    file_paths = []
    delete_file_paths = []

    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
        st.sidebar.write(f"Uploaded: {uploaded_file.name}")

    for delete_file in delete_files:
        delete_file_path = os.path.join(temp_dir, delete_file.name)
        with open(delete_file_path, "wb") as f:
            f.write(delete_file.getbuffer())
        delete_file_paths.append(delete_file_path)
        st.sidebar.write(f"Marked for deletion: {delete_file.name}")

    with st.spinner("Processing PDFs..."):
        try:
            rag.load_database(file_paths=file_paths, delete_file_paths=delete_file_paths)
            st.success("PDFs processed and vector store updated!")
        except Exception as e:
            st.error(f"Error processing PDFs: {str(e)}")
            st.write(traceback.format_exc())

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI for querying
st.title("Talk with your Document")
st.subheader("Chat History")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        st.write(message.content)

# Query input
query = st.text_input("Ask a question about the documents:", placeholder="e.g., What is the company's vision?")
if st.button("Search") and query:
    with st.spinner("Generating response..."):
        try:
            # Use the RAG class method directly with use_cache parameter
            result = rag.rag_chat(
                query=query, 
                use_cache=use_cache, 
                conversation_id="streamlit_conversation"
            )

            # Update session state with new messages from RAG chat history
            st.session_state.messages = rag.chat_history.copy()

            # Display the response
            st.subheader("Response")
            st.write(result["decision"]) 

            st.subheader("Sources")
            st.json({"sources": result["sources"]})
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            st.write(traceback.format_exc())
else:
    if not query:
        st.warning("Please enter a query.")
    if not rag.vector_store_manager.get_vector_store():
        st.warning("Please upload and process PDF files or load default PDFs from config.")