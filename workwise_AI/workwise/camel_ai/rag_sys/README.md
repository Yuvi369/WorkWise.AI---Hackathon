# RAG & CAG Document Q&A System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) and Cache-Augmented Generation (CAG) system for question answering on PDF documents. The system loads PDF documents, chunks them into manageable pieces, creates vector embeddings, and uses a language model to generate answers based on retrieved context. It includes a semantic caching mechanism to improve response efficiency by storing and retrieving responses for similar queries.

## Author

**Kaviya M**

## Project Structure

- `setup_environment.py`: Loads Google API key from .env.
- `load_and_process_document.py`: Loads and splits a PDF into chunks.
- `vectorstore_manager.py`: Manages the FAISS vector store, including creation, document addition, deletion, and persistence.
- `metadata_manager.py`: Handles metadata operations, such as tracking processed files and their hashes to avoid duplicates.
- `compute_file_hash.py`: Computes MD5 hashes for files to identify unique content.
- `config_loader.py`: Loads configuration from config.yaml.
- `delete_document.py`: Implements logic to delete documents from the vector store based on file hashes.
- `langfuse_prompt.py`: Fetches system prompts from Langfuse for use in the RAG pipeline.
- `rag_chain.py`: Implements the question-answering pipeline, integrating document retrieval, language model generation, and semantic caching for optimized performance.
- `semantic_cache.py`: Provides semantic caching to store and retrieve query-response pairs based on similarity.
- `main.py`: Orchestrates the pipeline, processing files, handling deletions, and running queries.

## Prerequisites

- Python 3.8+

## Installation

Install dependencies:
```bash
pip install faiss-cpu langchain-community langchain-google-genai langchain-huggingface langchain python-dotenv sentence-transformers langfuse
```

## Usage

Run the main script:
```bash
python main.py
```

## Example Queries

- "What is the recruitment strategy of SPIL?"
- "What is the salary procedure?"
- "What are the leave policies?"

## Features

- **Document Processing**: Loads and chunks PDF documents for efficient retrieval using load_and_process_document.py.
- **Vector Store Management**: Uses VectorStoreManager to handle FAISS vector store operations with sentence-transformers/all-mpnet-base-v2 embeddings for fast similarity search.
- **Metadata Management**: Employs MetadataManager to track processed files and their hashes, ensuring no duplicate processing.
- **File Deletion**: Supports deletion of documents from the vector store by file hash, with metadata cleanup.
- **Prompt Management**: Fetches system prompts from Langfuse using langfuse_prompt.py to format language model responses.
- **Language Model**: Utilizes gemini-2.0-flash for generating concise, context-aware answers.
- **Semantic Caching (CAG)**: Implements a SemanticCache class to store query-response pairs, using cosine similarity (threshold: 0.80) to retrieve cached responses for similar queries, reducing latency and API usage.
- **Cache Management**: Supports a maximum cache size (default: 100 entries) with a FIFO eviction policy to manage storage.
- **Langfuse Integration**: Logs interactions with Langfuse for observability, using user-specific metadata (e.g., langfuse_user_id: kaviya).

## Notes

- Ensure the PDF paths in config.yaml (e.g., document_file_paths, delete_file_path) are correct and accessible.
- The semantic cache is stored in rag_cache.json by default and uses a similarity threshold of 0.80 for cache hits.
- Caching can be disabled by setting use_cache=False in config.yaml.
- The system uses sentence-transformers/all-mpnet-base-v2 for embeddings and gemini-2.0-flash for response generation.
- Metadata is stored in vectorstore/metadata.json to track processed files and their hashes.
- File paths are normalized to handle platform-specific separators, ensuring cross-platform compatibility.
- Langfuse prompts are fetched using the prompt name specified in config.yaml (e.g., rag_prompt_name).

## Troubleshooting

- **API Key Error**: Verify GOOGLE_API_KEY in .env.
- **PDF Not Found**: Check the file path in main.py.
- **Dependency Issues**: Run pip list to confirm packages.
- **Cache Issues**: If cached responses are not retrieved as expected, check the similarity threshold (default: 0.80) or clear the rag_cache.json file.
- **Vector Store Errors**: Ensure vectorstore directory is accessible and not corrupted. Delete it to recreate the vector store if needed.
- **Langfuse Prompt Errors**: Ensure the prompt name in config.yaml exists in Langfuse and that API keys are correctly configured in .env.

## References

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [FAISS Documentation](https://faiss.ai/index.html)
- [Sentence Transformers](https://huggingface.co/sentence-transformers)
- [Langfuse](https://langfuse.com/docs)