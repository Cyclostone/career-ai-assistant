"""
Simple script to view data from the database.

Usage: python view_data.py leads
       python view_data.py knowledge_gaps
       python view_data.py stats
"""

import sys
from database import get_all_leads, get_all_knowledge_gaps, get_stats
from datetime import datetime

def view_leads():
    """Display all leads in a formatted table"""
    leads = get_all_leads()

    if not leads:
        print("No leads found in database")
        return

    print(f"\n📧 Total Leads: {len(leads)}\n")
    print("="*100)

    for lead in leads:
        print(f"ID: {lead['id']}")
        print(f"Email: {lead['email']}")
        print(f"Name: {lead['name']}")
        print(f"Notes: {lead['notes']}")
        print(f"Timestamp: {lead['timestamp']}")
        print("-" * 100)

def view_knowledge_gaps():
    """Display all knowledge gaps."""
    gaps = get_all_knowledge_gaps()

    if not gaps:
        print("✅ No knowledge gaps found in database.")
        return 
    
    print(f"\n🧠 Total Knowledge Gaps: {len(gaps)}\n")
    print("=" * 100)

    for gap in gaps:
        print(f"ID: {gap['id']}")
        print(f"Question: {gap['question']}")
        print(f"Timestamp: {gap['timestamp']}")
        print("-" * 100)

def view_stats():
    """Display database statistics."""
    stats = get_stats()

    print("\n📊 Database Statistics\n")
    print("=" * 50)
    print(f"Total Leads: {stats['total_leads']}")
    print(f"Total Knowledge Gaps: {stats['total_knowledge_gaps']}")
    print("=" * 50)

def main():
    if len(sys.argv) < 2:
        print("Usage: python view_data.py [leads|gaps|stats]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "leads":
        view_leads()
    elif command == "gaps":
        view_knowledge_gaps()
    elif command == "stats":
        view_stats()
    else:
        print(f"Unknown command: {command}")
        print(f"Available commands: leads, gaps, stats")
        sys.exit(1)

if __name__ == "__main__":
    main()
