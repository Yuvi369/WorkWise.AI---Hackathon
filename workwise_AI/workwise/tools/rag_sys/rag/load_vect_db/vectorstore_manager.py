import os
import faiss
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from rag_sys.rag.load_vect_db.delete_document import delete_by_filehash

class VectorStoreManager:
    def __init__(self, persist_directory, embedding_model):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name= embedding_model)
        self.vector_store = self._load_or_create_vector_store()
        self.metadata_file = os.path.join(persist_directory, "metadata.json")

    def _load_or_create_vector_store(self):
        """Loads an existing vector store or creates a new one."""
        if os.path.exists(self.persist_directory):
            print("Loading existing FAISS vector store...")
            vector_store = FAISS.load_local(
                self.persist_directory,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Loaded {vector_store.index.ntotal} vectors.")
            return vector_store
        else:
            print("Creating new FAISS vector store...")
            embedding_dim = len(self.embeddings.embed_query("test"))
            index = faiss.IndexFlatL2(embedding_dim)
            return FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={}
            )

    def add_documents(self, splits):
        """Adds documents to the vector store."""
        if splits:
            print(f"Adding {len(splits)} new documents...")
            self.vector_store.add_documents(documents=splits)
            print(f"Now storing {self.vector_store.index.ntotal} vectors.")

    def delete_documents(self, file_hash, metadata_manager):
        """Deletes documents by file hash."""
        if not self.vector_store:
            return False
        return delete_by_filehash(self.vector_store, file_hash, self.metadata_file)

    def save(self):
        """Saves the vector store to disk."""
        if self.vector_store and self.vector_store.index.ntotal > 0:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.vector_store.save_local(self.persist_directory)
            print("Saved FAISS vector store.")

    def get_vector_store(self):
        """Returns the vector store instance."""
        if not self.vector_store:
            raise ValueError("Vector store not initialized.")
        return self.vector_store