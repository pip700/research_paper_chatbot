from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os
import shutil

def get_embedding_function():
    """Initializes the embedding model."""
    # Using a cache directory for the model can speed up subsequent runs
    model_kwargs = {'device': 'cpu'} # Use CPU for embedding
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def initialize_vector_store(persist_directory: str = "./chroma_db", clear: bool = False):
    """Initialize or load existing vector store"""
    if clear and os.path.exists(persist_directory):
        print(f"Clearing old vector store at: {persist_directory}")
        shutil.rmtree(persist_directory)

    os.makedirs(persist_directory, exist_ok=True)

    embedding_model = get_embedding_function()

    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )

def add_texts_to_store(vector_store, texts: list):
    """Add texts to the vector store"""
    if not texts:
        raise ValueError("No texts provided to add to vector store")

    vector_store.add_texts(texts)
    print(f"Added {len(texts)} new chunks to the vector store.")
    vector_store.persist()

    return len(texts)

def search_similar_texts(vector_store, query: str, k: int = 4):
    """Search for similar texts in the vector store"""
    return vector_store.similarity_search(query, k=k)
