"""
Vector Store - ChromaDB operations for storing and searching document embeddings.
"""

import chromadb
from chromadb.config import Settings
from config import VECTOR_DB_DIR
from typing import List, Dict, Optional

# Initialize ChromaDB client with persistent storage
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)

# Collection name
COLLECTION_NAME = "career_knowledge"

def get_or_create_collection():
    """Get or create the career knowledge collection."""
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"✅ Loaded existing collection: {COLLECTION_NAME}")
    return collection

def add_documents(documents: List[str], metadatas: List[Dict], ids: List[str]):
    """
    Add documents to the vector store.
    
    Args:
        documents: List of text chunks to embed and store
        metadatas: List of metadata dicts for each document
        ids: List of unique IDs for each document
    """
    collection = get_or_create_collection()
    
    # ChromaDB handles batching internally, but we'll batch for safety
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_metas = metadatas[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        
        collection.add(
            documents=batch_docs,
            metadatas=batch_metas,
            ids=batch_ids
        )
        print(f"   📦 Added batch {i // batch_size + 1} ({len(batch_docs)} documents)")

def search_similar(query: str, n_results: int = 3) -> Dict:
    """
    Search for similar documents using semantic search.
    
    Args:
        query: The search query text
        n_results: Number of results to return
        
    Returns:
        Dict with documents, metadatas, distances, and ids
    """
    collection = get_or_create_collection()
    
    # Handle empty collection gracefully
    if collection.count() == 0:
        return {'documents': [[]], 'metadatas': [[]], 'distances': [[]], 'ids': [[]]}
    
    # Don't request more results than available
    actual_n = min(n_results, collection.count())
    
    results = collection.query(
        query_texts=[query],
        n_results=actual_n,
        include=["documents", "metadatas", "distances"]
    )
    
    return results

def get_collection_stats() -> Dict:
    """Get statistics about the vector store collection."""
    collection = get_or_create_collection()
    
    return {
        "collection_name": COLLECTION_NAME,
        "total_documents": collection.count(),
        "metadata": collection.metadata
    }

def reset_collection():
    """Delete and recreate the collection."""
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"🗑️  Deleted collection: {COLLECTION_NAME}")
    except Exception:
        pass
    
    return get_or_create_collection()

def list_collections():
    """List all collections in the database."""
    return [col.name for col in client.list_collections()]


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("Vector Store Test")
    print("=" * 60)
    
    # Get or create collection
    collection = get_or_create_collection()
    
    # Add test documents
    test_docs = [
        "I have 5 years of experience in Python development",
        "I worked at Google as a software engineer",
        "My skills include machine learning and data science"
    ]
    test_metas = [
        {"source": "test", "chunk_index": 0},
        {"source": "test", "chunk_index": 1},
        {"source": "test", "chunk_index": 2}
    ]
    test_ids = ["test_0", "test_1", "test_2"]
    
    add_documents(test_docs, test_metas, test_ids)
    
    # Search
    results = search_similar("What programming languages do you know?")
    print(f"\n🔍 Search Results:")
    for doc, meta, dist in zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ):
        print(f"  📄 {doc[:80]}... (distance: {dist:.4f})")
    
    # Stats
    stats = get_collection_stats()
    print(f"\n📊 Stats: {stats}")
    
    print("\n✅ Vector store test complete!")
