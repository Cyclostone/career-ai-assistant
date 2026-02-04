"""
Chat logic - loads knowledge and handles conversation.
"""

from pypdf import PdfReader
from config import openai_client, MODEL, ASSISTANT_NAME, KNOWLEDGE_DIR
from tools import tools, handle_tool_calls


# Load knowledge from files
def load_knowledge():
    """Load LinkedIn PDF and summary.txt."""
    linkedin = ""
    summary = ""
    
    # Load LinkedIn PDF
    try:
        reader = PdfReader(f"{KNOWLEDGE_DIR}/linkedin.pdf")
        for page in reader.pages:
            text = page.extract_text()
            if text:
                linkedin += text
    except FileNotFoundError:
        print("Warning: linkedin.pdf not found in data/knowledge/")
    
    # Load summary
    try:
        with open(f"{KNOWLEDGE_DIR}/summary.txt", "r", encoding="utf-8") as f:
            summary = f.read()
    except FileNotFoundError:
        print("Warning: summary.txt not found in data/knowledge/")
    
    return summary, linkedin


# Build system prompt
def build_system_prompt():
    """Create the system prompt with knowledge."""
    summary, linkedin = load_knowledge()
    
    prompt = f"""You are acting as {ASSISTANT_NAME}. You are answering questions on {ASSISTANT_NAME}'s website, \
particularly questions related to {ASSISTANT_NAME}'s career, background, skills and experience. \
Your responsibility is to represent {ASSISTANT_NAME} for interactions on the website as faithfully as possible. \
You are given a summary of {ASSISTANT_NAME}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool."""
    
    if summary:
        prompt += f"\n\n## Summary:\n{summary}"
    
    if linkedin:
        prompt += f"\n\n## LinkedIn Profile:\n{linkedin}"
    
    prompt += f"\n\nWith this context, please chat with the user, always staying in character as {ASSISTANT_NAME}."
    
    return prompt


# Main chat function
def chat(message, history):
    """
    Process a chat message and return the AI's response.
    """
    system_prompt = build_system_prompt()
    
    # Build messages list
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    
    done = False
    while not done:
        # Call OpenAI
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools
        )
        
        finish_reason = response.choices[0].finish_reason
        
        # If LLM wants to call tools
        if finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    
    return response.choices[0].message.content