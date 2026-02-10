"""
Tools - functions the AI can call.
Replaces notebook cells 4-14.
"""

import json
import requests
from config import PUSHOVER_USER, PUSHOVER_TOKEN, PUSHOVER_URL
from storage.database import add_lead, add_knowledge_gap


# Cell 4: Push notification function
def push(message):
    """Send a push notification via Pushover."""
    print(f"Push: {message}")
    if not PUSHOVER_USER or not PUSHOVER_TOKEN:
        print("Pushover not configured, skipping notification")
        return
    
    payload = {
        "user": PUSHOVER_USER,
        "token": PUSHOVER_TOKEN,
        "message": message
    }
    try:
        requests.post(PUSHOVER_URL, data=payload, timeout=2)
    except Exception as e:
        print(f"Push notification failed: {e}")


# Record user details
def record_user_details(email, name="Name not provided", notes="not provided"):
    """Record when a user wants to get in touch."""

    # Save to a database first
    add_lead(email, name, notes)

    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


# Record unknown question
def record_unknown_question(question):
    """Record a question that couldn't be answered."""

    # Save to database first
    add_knowledge_gap(question)

    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}


# Tool schemas for OpenAI
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# Tools list
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]


# Handle tool calls (using globals() like the notebook)
def handle_tool_calls(tool_calls):
    """Execute tool calls from the LLM."""
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        
        # Use globals() to find the function    
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    return results
