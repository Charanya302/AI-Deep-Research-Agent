from rag.vector_store import load_vector_store


def retrieve_documents(query, k=3):

    if not query or not query.strip():
        raise ValueError("Please enter a valid search query.")

    # Load existing ChromaDB vector store
    vector_store = load_vector_store()

    # Search for semantically similar documents
    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results