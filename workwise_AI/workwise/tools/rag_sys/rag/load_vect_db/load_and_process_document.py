from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_and_process_document(file_path: str):
    """Loads a PDF document and splits it into chunks for processing."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        print("Splitting document into chunks...")
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Add PDF name and ensure page number in metadata
        pdf_name = os.path.basename(file_path)
        for doc in docs:
            doc.metadata['pdf_name'] = pdf_name
            if 'page' not in doc.metadata:
                doc.metadata['page'] = 0
                
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        return text_splitter.split_documents(docs)
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to load or process the PDF: {str(e)}")