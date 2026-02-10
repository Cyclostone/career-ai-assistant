"""
Cache - Semantic caching for cost optimization
Stores responses to similar queries to reduce API calls and costs.
"""

from functools import cache
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict
from diskcache import Cache
from datetime import datetime

# Cache configuration
CACHE_DIR = "data/cache"
CACHE_SIZE_LIMIT = 5 * 1024 * 1024 # 5 MB
CACHE_TTL = 7 * 24 * 60 * 60 # 7 days

def get_cache():
    """Get or create the disk cache."""
    cache_path = Path(CACHE_DIR)
    cache_path.mkdir(parents=True, exist_ok=True)
    return Cache(
        str(cache_path),
        size_limit=CACHE_SIZE_LIMIT,
        eviction_policy="least-recently-used",
    )

def generate_cache_key(query: str, context: str) -> str:
    """
    Generate a cache key from query and context.
    Uses hash to create consistent keys for similar inputs.
    
    Args:
        query: User's query
        context: Retrieved context
    
    Returns:
        Hash string to use as cache key
    """
    # Combine query and context for cache key
    combined = f"{query.lower().strip()}|{context}"

    # Generate SHA256 hash
    return hashlib.sha256(combined.encode()).hexdigest()

def get_cached_response(query: str, context: str) -> Optional[str]:
    """
    Try to retrieve a cached response.
    
    Args:
        query: User's query
        context: Retrieved context
    
    Returns:
        Cached response dict if found, None otherwise
    """
    cache = get_cache()
    cache_key = generate_cache_key(query, context)

    cached = cache.get(cache_key)
    if cached:
        print(f"✅ Cache HIT for query: {query[:50]}...")
        return cached
    
    print(f"❌ Cache MISS for query: {query[:50]}...")
    return None

def set_cached_response(query: str, context: str, response: str, metadata: Dict = None):
    """
    Store a response in the cache.

    Args:
        query: User's query
        context: Retrieved context
        response: LLM response
        metadata: Optional metadata
    """
    cache = get_cache()
    cache_key = generate_cache_key(query, context)

    cached_data = {
        "query": query,
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }

    cache.set(cache_key, cached_data, expire=CACHE_TTL)
    print(f"✅ Cache SET for query: {query[:50]}...")

def get_cache_stats() -> Dict:
    """Get cache statistics."""
    cache = get_cache()

    return {
        "total_entries": len(cache),
        "size_bytes": cache.volume(),
        "size_mb": round(cache.volume() / (1024 * 1024), 2),
        "cache_dir": CACHE_DIR
    }

def clear_cache():
    """Clear the cache."""
    cache = get_cache()
    cache.clear()
    print(f"🗑️  Cache cleared")

if __name__ == "__main__":
    print("Testing Cache System...")

    # Test cache
    test_query = "What is Arpit's experience?"
    test_context = "Some context here"
    test_response = "Arpit has extensive experience..."
    
    # Set cache
    set_cached_response(test_query, test_context, test_response)
    
    # Get cache
    cached = get_cached_response(test_query, test_context)
    print(f"\nCached response: {cached}")
    
    # Stats
    stats = get_cache_stats()
    print(f"\nCache stats: {stats}")
