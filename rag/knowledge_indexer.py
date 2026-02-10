"""
Knowledge Indexer - Loads documents, chunks them, and stores in vector database
"""

from json import load
import os
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from config import KNOWLEDGE_DIR
from rag.vector_store import add_documents, reset_collection, get_collection_stats

def chunk_text(text: str, chunk_size: int=500, overlap: int=50) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: The text to chunk
        chunk_size: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        if end < text_length:
            # Look for sentence endings in the last 100 characters
            last_period = text.rfind('.', start, end)
            last_newline = text.rfind('\n', start, end)
            break_point = max(last_period, last_newline)

            if break_point > start:
                end = break_point + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap

    return chunks

def load_pdf(file_path: str) -> str:
    """
    Load a PDF file and return its text content.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def load_text_file(file_path: str) -> str:
    """
    Load text from a plain text file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def index_knowledge_base(reset: bool=False):

    """
    Load all knowledge documents, chunk them, and store in vector database.
    
    Args:
        reset: If True, clear existing collection before indexing
    """
    if reset:
        print("🗑️  Resetting vector database...")
        reset_collection()

    knowledge_dir = Path(KNOWLEDGE_DIR)

    if not knowledge_dir.exists():
        print(f"⚠️ Knowledge directory not found: {knowledge_dir}")
        return
    
    all_documents = []
    all_metadatas = []
    all_ids = []
    chunk_counter = 0

    # Process all files in knowledge directory
    for file_path in knowledge_dir.iterdir():
        if file_path.is_file():
            print(f"\n📄 Processing: {file_path.name}")

        try:
            # Load Document based on file type
            if file_path.suffix.lower() == ".pdf":
                text = load_pdf(str(file_path))
                source_type = "PDF"
            elif file_path.suffix.lower() in ['.txt', '.md']:
                text = load_text_file(str(file_path))
                source_type = "Text"
            else:
                print(f"   ⏭️ Skipping unsupported file type: {file_path.suffix}")
                continue
            
            # Chunk the document
            chunks = chunk_text(text, chunk_size=500, overlap=50)
            print(f"   ✂️  Created {len(chunks)} chunks")

            # Create metadata and IDs for each chunk
            for i, chunk in enumerate(chunks):
                all_documents.append(chunk)
                all_metadatas.append({
                    "source": file_path.name,
                    "source_type": source_type,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
                all_ids.append(f"{file_path.stem}_chunk_{chunk_counter}")
                chunk_counter += 1

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")

    # Add all documents to vector store
    if all_documents:
        print(f"\n💾 Storing {len(all_documents)} chunks in vector database...")
        add_documents(all_documents, all_metadatas, all_ids)

        # Show Stats
        stats = get_collection_stats()
        print(f"\n✅ Indexing complete!")
        print(f"   📊 Total documents in database: {stats['total_documents']}")
    else:
        print(f"\n⚠️  No documents found to index")


if __name__ == "__main__":
    print("="*60)
    print(f"Knowledge Base Indexer")
    print("="*60)

    # Index the knowledge base (reset=True to start fresh)
    index_knowledge_base(reset=True)

    print("="*60)
    print("\nKnowledge base indexing complete!")
    print("="*60)
