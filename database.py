"""
Database operations for storing leads, conversations, and knowledge gaps.
Uses SQLite for simple, file-based persistence.
"""

import sqlite3
from config import DATABASE_PATH
from datetime import datetime
from pathlib import Path

def get_connection():
    """Get a database connection and ensure tables exist."""
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    _create_tables(conn)
    return conn

def _create_tables(conn):
    """Create tables if they don't exist"""
    cursor = conn.cursor()

    # Leads table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        name TEXT,
        notes TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Knowledge gaps table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    """)

    # Conversations table (for future use)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            message TEXT,
            role TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

def add_lead(email, name="Name not provided", notes="not provided"):
    """
    Add a new lead to the database.

    Args:
        email (str): User's email address
        name (str): User's name (optional)
        notes (str): Additional context about the conversation (optional)
    
    Returns:
        The ID of the inserted lead
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO leads (email, name, notes) VALUES (?, ?, ?)",
        (email, name, notes)
    )

    lead_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"✅ Lead saved to database: {email} (ID: {lead_id})")
    return lead_id

def add_knowledge_gap(question):
    """
    Record a question that couldn't be answered.

    Args:
        question: The unanswered question

    Returns:
        The ID of the inserted record
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO knowledge_gaps (question) VALUES (?)",
        (question,)
    )

    gap_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"✅ Knowledge gap saved to database: {question} (ID: {gap_id})")
    return gap_id

def get_all_leads():
    """Get all leads from the database,"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads ORDER BY timestamp DESC")
    leads = cursor.fetchall()
    conn.close()

    return [dict(lead) for lead in leads]

def get_recent_leads(limit=10):
    """Get the most recent leads."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads ORDER BY timestamp DESC LIMIT ?", (limit,))
    leads = cursor.fetchall()
    conn.close()

    return [dict(lead) for lead in leads]

def get_all_knowledge_gaps():
    """Get all knowledge gaps from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM knowledge_gaps ORDER BY timestamp DESC"
    )

    gaps = cursor.fetchall()
    conn.close()

    return [dict(gap) for gap in gaps]

def get_stats():
    """Get Database statistics."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS lead_count FROM leads")
    lead_count = cursor.fetchone()["lead_count"]

    cursor.execute("SELECT COUNT(*) AS gap_count FROM knowledge_gaps")
    gap_count = cursor.fetchone()["gap_count"]

    conn.close()

    return {
        "total_leads": lead_count,
        "total_knowledge_gaps": gap_count
    }
    
