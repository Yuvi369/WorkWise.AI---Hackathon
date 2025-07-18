import json
import time
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticCache:
    def __init__(self, json_file: str, threshold: int, max_size: int, eviction_policy="FIFO"):
        """Initializes the semantic cache."""
        self.index = faiss.IndexFlatIP(768) 
        self.encoder = SentenceTransformer("all-mpnet-base-v2")
        self.cosine_threshold = threshold  
        self.json_file = json_file
        self.max_size = max_size
        self.eviction_policy = eviction_policy
        
        self.cache = self._retrieve_cache()
        
        # Add existing embeddings to the index (normalized)
        if self.cache["embeddings"]:
            embeddings_array = np.array(self.cache["embeddings"], dtype=np.float32)
            faiss.normalize_L2(embeddings_array)
            self.index.add(embeddings_array)
    
    def _retrieve_cache(self):
        """Retrieves the cache from a JSON file."""
        try:
            with open(self.json_file, "r") as file:
                cache = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            cache = {"queries": [], "embeddings": [], "responses": [], "metadata": []}
        return cache
    
    def _store_cache(self):
        """Stores the cache to a JSON file."""
        with open(self.json_file, "w") as file:
            json.dump(self.cache, file)
    
    def _evict(self):
        """Evicts items from the cache based on the eviction policy."""
        if len(self.cache["queries"]) > self.max_size:
            num_to_remove = len(self.cache["queries"]) - self.max_size
            if self.eviction_policy == "FIFO":
                # Remove the oldest entries
                self.cache["queries"] = self.cache["queries"][num_to_remove:]
                self.cache["responses"] = self.cache["responses"][num_to_remove:]
                self.cache["metadata"] = self.cache["metadata"][num_to_remove:]
                
                # For embeddings, we need to rebuild the FAISS index
                self.cache["embeddings"] = self.cache["embeddings"][num_to_remove:]
                self.index = faiss.IndexFlatIP(768)
                if self.cache["embeddings"]:
                    embeddings_array = np.array(self.cache["embeddings"], dtype=np.float32)
                    faiss.normalize_L2(embeddings_array)
                    self.index.add(embeddings_array)
    
    def get(self, query):
        """Attempts to retrieve a response from the cache based on semantic similarity."""
        start_time = time.time()
        
        query_embedding = self.encoder.encode([query])
        faiss.normalize_L2(query_embedding) 
        
        if self.index.ntotal > 0: 
            D, I = self.index.search(query_embedding, 1)
            
            if I[0][0] >= 0 and D[0][0] >= self.cosine_threshold: 
                idx = int(I[0][0])
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                return {
                    "found": True,
                    "response": self.cache["responses"][idx],
                    "similarity_score": float(D[0][0]),
                    "original_query": self.cache["queries"][idx],
                    "metadata": self.cache["metadata"][idx],
                    "time": elapsed_time
                }
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            return {
                "found": False,
                "similarity_score": float(D[0][0]),
                "time": elapsed_time
            }
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        return {
            "found": False,
            "similarity_score": 0.0,
            "time": elapsed_time
        }
    
    def add(self, query, response, metadata=None):
        """Adds a query-response pair to the cache."""

        query_embedding = self.encoder.encode([query])
        faiss.normalize_L2(query_embedding)  
        
        # Add to cache
        self.cache["queries"].append(query)
        self.cache["embeddings"].append(query_embedding[0].tolist())
        self.cache["responses"].append(response)
        self.cache["metadata"].append(metadata or {})
        
        # Add to FAISS index
        self.index.add(query_embedding)
        
        self._evict()
        self._store_cache()


# import json
# import time
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# class SemanticCache:
#     def __init__(self, json_file: str, threshold: int, max_size: int, eviction_policy="FIFO"):
#         """Initializes the semantic cache."""
#         self.index = faiss.IndexFlatIP(768) 
#         self.encoder = SentenceTransformer("all-mpnet-base-v2")
#         self.cosine_threshold = threshold  
#         self.json_file = json_file
#         self.max_size = max_size
#         self.eviction_policy = eviction_policy
        
#         self.cache = self._retrieve_cache()
        
#         # Add existing embeddings to the index (normalized)
#         if self.cache["embeddings"]:
#             embeddings_array = np.array(self.cache["embeddings"], dtype=np.float32)
#             faiss.normalize_L2(embeddings_array)
#             self.index.add(embeddings_array)
    
#     def _retrieve_cache(self):
#         """Retrieves the cache from a JSON file."""
#         try:
#             with open(self.json_file, "r") as file:
#                 cache = json.load(file)
#         except (FileNotFoundError, json.JSONDecodeError):
#             cache = {
#                 "queries": [], 
#                 "contextual_queries": [],  # Store concatenated query with history
#                 "embeddings": [], 
#                 "responses": [], 
#                 "metadata": []
#             }
#         return cache
    
#     def _store_cache(self):
#         """Stores the cache to a JSON file."""
#         with open(self.json_file, "w") as file:
#             json.dump(self.cache, file)
    
#     def _evict(self):
#         """Evicts items from the cache based on the eviction policy."""
#         if len(self.cache["queries"]) > self.max_size:
#             num_to_remove = len(self.cache["queries"]) - self.max_size
#             if self.eviction_policy == "FIFO":
#                 # Remove the oldest entries
#                 self.cache["queries"] = self.cache["queries"][num_to_remove:]
#                 self.cache["contextual_queries"] = self.cache["contextual_queries"][num_to_remove:]
#                 self.cache["responses"] = self.cache["responses"][num_to_remove:]
#                 self.cache["metadata"] = self.cache["metadata"][num_to_remove:]
                
#                 # For embeddings, rebuild the FAISS index
#                 self.cache["embeddings"] = self.cache["embeddings"][num_to_remove:]
#                 self.index = faiss.IndexFlatIP(768)
#                 if self.cache["embeddings"]:
#                     embeddings_array = np.array(self.cache["embeddings"], dtype=np.float32)
#                     faiss.normalize_L2(embeddings_array)
#                     self.index.add(embeddings_array)
    
#     def get(self, query, messages=None):
#         """Attempts to retrieve a response from the cache based on semantic similarity with context."""
#         start_time = time.time()
        
#         # Create a contextual query by concatenating messages and the current query
#         contextual_query = ""
#         if messages:
#             # Concatenate the last few messages (e.g., last 2 for context) and the query
#             for msg in messages[-2:]:  # Limit to last 2 messages for brevity
#                 role = "Human" if msg["role"] == "user" else "Assistant"
#                 contextual_query += f"{role}: {msg['content']}\n"
#         contextual_query += f"Human: {query}"
        
#         # Encode the contextual query
#         query_embedding = self.encoder.encode([contextual_query])
#         faiss.normalize_L2(query_embedding) 
        
#         if self.index.ntotal > 0: 
#             # Search for top-3 most similar embeddings
#             D, I = self.index.search(query_embedding, 3)
            
#             # Check if all top-3 similarity scores are >= 0.8
#             if I[0][0] >= 0 and all(score >= 0.8 for score in D[0]): 
#                 idx = int(I[0][0])  # Use the top-1 match
                
#                 end_time = time.time()
#                 elapsed_time = end_time - start_time
                
#                 return {
#                     "found": True,
#                     "response": self.cache["responses"][idx],
#                     "similarity_score": float(D[0][0]),
#                     "original_query": self.cache["queries"][idx],
#                     "metadata": self.cache["metadata"][idx],
#                     "time": elapsed_time
#                 }
            
#             end_time = time.time()
#             elapsed_time = end_time - start_time
            
#             return {
#                 "found": False,
#                 "similarity_score": float(D[0][0]) if len(D[0]) > 0 else 0.0,
#                 "time": elapsed_time
#             }
        
#         end_time = time.time()
#         elapsed_time = end_time - start_time
        
#         return {
#             "found": False,
#             "similarity_score": 0.0,
#             "time": elapsed_time
#         }
    
#     def add(self, query, response, metadata=None, messages=None):
#         """Adds a query-response pair to the cache with contextual query."""
#         # Create contextual query for embedding
#         contextual_query = ""
#         if messages:
#             for msg in messages[-2:]:  # Limit to last 2 messages
#                 role = "Human" if msg["role"] == "user" else "Assistant"
#                 contextual_query += f"{role}: {msg['content']}\n"
#         contextual_query += f"Human: {query}"
        
#         query_embedding = self.encoder.encode([contextual_query])
#         faiss.normalize_L2(query_embedding)  
        
#         # Add to cache
#         self.cache["queries"].append(query)
#         self.cache["contextual_queries"].append(contextual_query)
#         self.cache["embeddings"].append(query_embedding[0].tolist())
#         self.cache["responses"].append(response)
#         self.cache["metadata"].append(metadata or {})
        
#         # Add to FAISS index
#         self.index.add(query_embedding)
        
#         self._evict()
#         self._store_cache()