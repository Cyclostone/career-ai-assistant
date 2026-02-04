"""
Configuration - loads environment variables.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

# OpenAI client
openai_client = OpenAI()

# Pushover credentials
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

# Your identity
ASSISTANT_NAME = "Arpit Shrotriya"
ASSISTANT_EMAIL = "arpit.shrotriya5945@gmail.com"

# Model settings
MODEL = "gpt-4o-mini"

# Paths
KNOWLEDGE_DIR = "data/knowledge"
DATABASE_PATH = "Data/leads.db"