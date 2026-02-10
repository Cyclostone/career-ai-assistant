"""
Gradio app - the main entry point.
"""

import gradio as gr
from core.chat import chat
from rag.vector_store import get_collection_stats
from rag.knowledge_indexer import index_knowledge_base

# Auto-index knowledge base if vector store is empty
try:
    stats = get_collection_stats()
    if stats["total_documents"] == 0:
        print("📚 Vector store empty — auto-indexing knowledge base...")
        index_knowledge_base(reset=False)
    else:
        print(f"✅ Vector store has {stats['total_documents']} documents")
except Exception as e:
    print(f"⚠️ Knowledge indexing skipped: {e}")

# Launch Gradio interface
if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch()