"""
Retriever - Semantic search retrieval from vector database.
"""

from typing import Dict, List
from rag.vector_store import search_similar


def format_context_for_llm(results: List[Dict]) -> str:
    """
    Format retrieved results into a context string for the LLM.
    
    Args:
        results: List of filtered result dicts with document, metadata, distance
        
    Returns:
        Formatted context string
    """
    if not results:
        return "No relevant context found in knowledge base."
    
    context_parts = []
    context_parts.append("=== RELEVANT CONTEXT FROM KNOWLEDGE BASE ===\n")
    
    for i, result in enumerate(results, 1):
        source = result['metadata'].get('source', 'Unknown')
        relevance = result.get('relevance_score', 0)
        context_parts.append(f"--- Source {i}: {source} (relevance: {relevance:.2f}) ---")
        context_parts.append(result['document'])
        context_parts.append("")
    
    context_parts.append("=== END OF CONTEXT ===")
    return "\n".join(context_parts)


def retreive_context(query: str, top_k: int=3, min_relevance: float=0.0) -> Dict:
    """
    Retrieve relevant context for a query from the vector database.
    
    Args:
        query: The user's question
        top_k: Number of results to retrieve
        min_relevance: Minimum relevance score (0-1) to include
        
    Returns:
        Dict with query, results, formatted_context, and num_results
    """
    # Search vector database
    results = search_similar(query, n_results=top_k)
    
    # Extract results
    documents = results['documents'][0] if results['documents'] else []
    metadatas = results['metadatas'][0] if results['metadatas'] else []
    distances = results['distances'][0] if results['distances'] else []
    
    # Filter by relevance (cosine distance: 0 = identical, 2 = opposite)
    filtered_results = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        max_distance = 2.0
        if dist <= max_distance:
            filtered_results.append({
                'document': doc,
                'metadata': meta,
                'distance': dist,
                'relevance_score': max(0, 1.0 - (dist / 2.0))
            })
    
    # Format context for LLM
    formatted_context = format_context_for_llm(filtered_results)
    
    return {
        'query': query,
        'results': filtered_results,
        'formatted_context': formatted_context,
        'num_results': len(filtered_results)
    }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("Retriever Test")
    print("=" * 60)
    
    test_queries = [
        "What is your experience?",
        "Tell me about your skills",
        "What projects have you worked on?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result = retreive_context(query)
        print(f"   📊 Found {result['num_results']} relevant chunks")
        if result['results']:
            for r in result['results']:
                print(f"   📄 [{r['metadata']['source']}] relevance: {r['relevance_score']:.2f}")
                print(f"      {r['document'][:100]}...")
    
    print("\n✅ Retriever test complete!")
