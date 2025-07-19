import sys
import os

# Dynamically add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
import traceback
from typing import List
from camel_ai.rag_sys.rag.utils.common import normalize_file_paths
from camel_ai.rag_sys.rag.chat.rag_chain import rag_chain
from camel_ai.rag_sys.rag.load_vect_db.load_and_process_document import load_and_process_document
from camel_ai.rag_sys.rag.load_vect_db.metadata_manager import MetadataManager
from camel_ai.rag_sys.rag.load_vect_db.vectorstore_manager import VectorStoreManager
from camel_ai.rag_sys.rag.utils.compute_file_hash import compute_file_hash
from camel_ai.rag_sys.rag.utils.config_loader import load_config

class RAG:

    def __init__(self):
        self.config = load_config()
        self.persist_directory = self.config["vector_db"]["vectorstore_path"]
        self.embedding_model = self.config["vector_db"]["embedding_model"]
        self.metadata_file = os.path.join(self.persist_directory, "metadata.json")
        # Initialize managers
        self.vector_store_manager = VectorStoreManager(self.persist_directory, self.embedding_model)
        self.metadata_manager = MetadataManager(self.metadata_file)

    def load_database(self, file_paths=None, delete_file_paths=None):
        try:
            # Normalize file paths
            file_paths = normalize_file_paths(
                file_paths or self.config["app"].get(
                    "document_file_paths", self.config["app"].get("document_file_path")
                )
            )
            delete_file_paths = normalize_file_paths(
                delete_file_paths or self.config["app"].get("delete_file_path")
            )
            # Handle deletions
            for delete_file_path in delete_file_paths:
                print(f"\nDeleting : {delete_file_path}")
                if not os.path.exists(delete_file_path):
                    print(f"File {delete_file_path} does not exist. Skipping deletion.")
                    continue
                file_hash = compute_file_hash(delete_file_path)
                if self.vector_store_manager.delete_documents(file_hash, self.metadata_manager):
                    print(f"Deleted documents for file: {delete_file_path}.")
                    self.metadata_manager.remove_by_hash(file_hash)
                else:
                    print(f"No documents found for file: {delete_file_path}.")

            # Process new documents
            for file_path in file_paths:
                print(f"\nProcessing file: {file_path}")
                file_hash = compute_file_hash(file_path)
                if self.metadata_manager.has_hash(file_hash):
                    print(f"File content already processed. Skipping...")
                    if not self.metadata_manager.has_file_path(file_path):
                        self.metadata_manager.add_entry(file_path, file_hash)
                else:
                    print(f"Adding new file {file_path} to vector store...")
                    splits = load_and_process_document(file_path)
                    print(f"Split document into {len(splits)} chunks.")
                    self.vector_store_manager.add_documents(splits)
                    self.metadata_manager.add_entry(file_path, file_hash)
            # Save changes
            self.vector_store_manager.save()
            self.metadata_manager.save()

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            traceback.print_exc()

    def rag_chat(self, query=None, top_k=None, use_cache=None):
        try:
            if query is None:
                query = input("Your question: ")
            if not query or not query.strip():
                print("Please enter a valid question.")
                return None
            
            top_k = top_k or self.config["app"]["top_k"]
            use_cache = use_cache if use_cache is not None else self.config["app"].get("use_cache", False)
            prompt_name = self.config["app"]["rag_prompt_name"]
            vector_store = self.vector_store_manager.get_vector_store()

            response = rag_chain(
                vector_store,
                query,
                top_k,
                use_cache,
                prompt_name
            )
            response_dict = {
                "decision": response["response"],
                "sources": [
                    {
                        "pdf_name": source["pdf_name"],
                        "page_number": source["page_number"],
                        "page_content": source.get("page_content", "Content not available")
                    } for source in response["sources"]
                ]
            }
            print("\nQuery:", query)
            print("\nResponse:", response_dict["decision"])
            print("\nSources:")
            print(response_dict["sources"])
            return response_dict
        
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            traceback.print_exc()

    def rag_agent_main(self, query):
        self.load_database()
        return self.rag_chat(query=query)


if __name__ == "__main__":
    inp_prompt = """
        ticket_description = "This is a financial ticket involving secure account migration and transaction validation."

        employee_profile = {
            "employee_name": "Divya",
            "designation": "Intern",
            "department": "Development"
        }
    """
    rag = RAG()
    rag.load_database()
    rag.rag_chat(query=inp_prompt)
