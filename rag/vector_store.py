from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DB_PATH = "data/chroma_db"

COLLECTION_NAME = "research_documents"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def create_vector_store(chunks):

    if not chunks:
        raise ValueError("No text chunks available.")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    # Remove previous collection to prevent duplicate uploads
    try:
        existing_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=DB_PATH
        )

        existing_store.delete_collection()

    except Exception as e:
        print("Previous collection cleanup:", e)

    # Create fresh vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME
    )

    return vector_store


def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=DB_PATH
    )

    return vector_store