"""Storage - database and caching."""
from storage.database import add_lead, add_knowledge_gap, get_all_leads, get_all_knowledge_gaps, get_stats
from storage.cache import get_cached_response, set_cached_response, get_cache_stats
