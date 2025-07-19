import os
import time
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from camel_ai.rag_sys.rag.utils.langfuse_prompt import get_system_prompt
from camel_ai.rag_sys.rag.chat.semantic_cache import SemanticCache
from camel_ai.rag_sys.rag.llm_model.load import get_llm
from camel_ai.rag_sys.rag.utils.config_loader import load_config

_cache_instance = None
config = load_config()

def get_cache_instance():
    """Returns a singleton cache instance."""
    global _cache_instance
    cache_file = config["cache"]["cache_file"]
    threshold = config["cache"]["threshold"]
    max_size = config["cache"]["max_size"]
    if _cache_instance is None:
        _cache_instance = SemanticCache(
            json_file=cache_file, threshold=threshold, max_size=max_size
        )
    return _cache_instance

def rag_chain(vector_store, query: str, top_k: int, use_cache: bool, prompt_name: str):
    """Sets up a question-answering chain, retrieves context, and generates a response."""
    start_time = time.time()

    if use_cache:
        cache = get_cache_instance()
        cache_result = cache.get(query)
        if cache_result["found"]:
            print(f"Cache hit! Retrieved response with similarity score: {cache_result['similarity_score']:.4f}")
            print(f"Original query: '{cache_result['original_query']}'")
            print(f"Cache retrieval time: {cache_result['time']:.3f} seconds")
            total_time = time.time() - start_time
            print(f"Total time: {total_time:.3f} seconds")
            return cache_result["response"]
        
        print(f"Cache miss! similarity score: {cache_result['similarity_score']:.4f}")
    else:
        # print("Cache disabled. Generating a response...")
        print("Generating a response...")

    model = config["llm"]["model"]
    llm = get_llm(model)

    # Fetch system prompt from Langfuse
    # system_prompt = get_system_prompt(prompt_name).replace("{{context}}", "{context}")
    system_prompt = get_system_prompt(prompt_name)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_start = time.time()
    documents = vector_store.similarity_search(query, k=top_k)
    retrieval_time = time.time() - retrieval_start
    print(f"Document retrieval time: {retrieval_time:.3f} seconds")

    # Extract source information
    sources = [
        {
            "pdf_name": doc.metadata.get("pdf_name", "Unknown"),
            "page_number": doc.metadata.get("page", 0) + 1,
            "page_content": doc.page_content
        }
        for doc in documents
    ]

    llm_start = time.time()
    response = question_answer_chain.invoke(
        {"input": query, "context": documents}
    )
    llm_time = time.time() - llm_start
    print(f"LLM response generation time: {llm_time:.3f} seconds")

    # Store in cache if enabled
    if use_cache:
        metadata = {"timestamp": time.time(), "prompt_name": prompt_name, "sources": sources}
        cache = get_cache_instance()
        cache.add(query, {"response": response, "sources": sources}, metadata)

    total_time = time.time() - start_time
    print(f"Total time: {total_time:.3f} seconds")
    
    return {
        "response": response,
        "sources": sources
    }