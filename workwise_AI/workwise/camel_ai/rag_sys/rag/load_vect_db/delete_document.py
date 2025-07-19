import os
import json
import numpy as np

def delete_by_filehash(vector_store, file_hash, metadata_file):
    """
    Deletes documents from the vector store that match the file path associated with the given file hash in metadata.json.
    Returns True if any documents were deleted, False otherwise.
    """
    deleted = False
    
    # Load metadata from metadata.json
    if not os.path.exists(metadata_file):
        print(f"Metadata file {metadata_file} does not exist.")
        return deleted
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    if not isinstance(metadata, list):
        metadata = [metadata]
    
    # Find file path(s) associated with the given file hash
    file_paths = [entry['file_path'] for entry in metadata if entry.get('file_hash') == file_hash]
    if not file_paths:
        return deleted
    
    # Get all document IDs and their metadata
    docstore = vector_store.docstore._dict
    index_to_docstore_id = vector_store.index_to_docstore_id
    ids_to_delete = []
    
    # Identify documents with matching file path in metadata
    for doc_id, doc in docstore.items():
        doc_metadata = doc.metadata
        doc_file_path = doc_metadata.get('source', '')
        if os.path.normpath(doc_file_path) in [os.path.normpath(fp) for fp in file_paths]:
            ids_to_delete.append(doc_id)
    
    # print("ids_to_delete", ids_to_delete)
    
    if ids_to_delete:
        # Find corresponding index IDs
        indices_to_delete = []
        for idx, doc_id in index_to_docstore_id.items():
            if doc_id in ids_to_delete:
                indices_to_delete.append(idx)
        
        # print("indices_to_delete", indices_to_delete)
        
        if indices_to_delete:
            # Remove from FAISS index
            indices_array = np.array(indices_to_delete, dtype=np.int64)
            vector_store.index.remove_ids(indices_array)
            
            # Remove from docstore
            for doc_id in ids_to_delete:
                if doc_id in vector_store.docstore._dict:
                    del vector_store.docstore._dict[doc_id]
            
            # Rebuild index_to_docstore_id mapping
            new_index_to_docstore_id = {}
            remaining_doc_ids = set(vector_store.docstore._dict.keys())
            
            # Rebuild the mapping with only existing documents
            index_counter = 0
            for old_idx, doc_id in sorted(index_to_docstore_id.items()):
                if doc_id in remaining_doc_ids and old_idx not in indices_to_delete:
                    new_index_to_docstore_id[index_counter] = doc_id
                    index_counter += 1
            
            # Replace the old mapping
            vector_store.index_to_docstore_id = new_index_to_docstore_id
            
            print(f"Removed {len(ids_to_delete)} documents associated with file paths: {file_paths}.")
            deleted = True
        else:
            print(f"No matching indices found for associated with file paths: {file_paths}.")
    else:
        print(f"No documents found in docstore for file paths {file_paths}.")
    
    return deleted