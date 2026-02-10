"""
Chat logic - loads knowledge and handles conversation.
"""

import re
from openai import BadRequestError
from config import openai_client, MODEL, ASSISTANT_NAME
from core.tools import tools, handle_tool_calls
from rag.retriever import retreive_context
from storage.cache import get_cached_response, set_cached_response


def clean_response(text: str) -> str:
    """Remove raw function call text that the model sometimes leaks into responses."""
    # Remove <function=...>{...} patterns
    text = re.sub(r'<function=\w+>\{[^}]*\}', '', text)
    # Remove any leftover <function=...> tags
    text = re.sub(r'<function=\w+>', '', text)
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text

# Build system prompt
def build_system_prompt(retrieved_context: str = "") -> str:
    """
    Build the system prompt with dynamically retrieved context.
    
    Args:
        retrieved_context: Context retrieved from vector database for current query
    """
    prompt = f"""You are acting as {ASSISTANT_NAME}. You are answering questions on {ASSISTANT_NAME}'s website, \
particularly questions related to {ASSISTANT_NAME}'s career, background, skills and experience. \
Your responsibility is to represent {ASSISTANT_NAME} for interactions on the website as faithfully as possible.
 
{retrieved_context}
 
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
Use the context provided above to answer questions accurately. Always cite sources when referencing specific information.
 
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool.
 
With this context, please chat with the user, always staying in character as {ASSISTANT_NAME}."""
    
    return prompt


# Main chat function
def chat(message, history):
    """
    Process a chat message with RAG-powered context retrieval.
    
    Args:
        message: User's current message
        history: Chat history from Gradio (list of [user_msg, assistant_msg] pairs)

    """
    user_query = message

    # Retrieve relevant context for this specific query
    retrieval_result = retreive_context(user_query, top_k=3)
    retrieved_context = retrieval_result['formatted_context']

    # Check cache first
    cached = get_cached_response(user_query, retrieved_context)
    if cached:
        return cached['response']
    
    # Build system prompt
    system_prompt = build_system_prompt(retrieved_context)
    
    # Build messages list (sanitize history to remove unsupported fields like metadata)
    clean_history = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    messages = [{"role": "system", "content": system_prompt}] + clean_history + [{"role": "user", "content": user_query}]
    
    done = False
    while not done:
        try:
            response = openai_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools
            )
        except BadRequestError as e:
            # Groq sometimes fails with tool_use_failed when model outputs raw function text
            # Retry without tools to get a normal response
            print(f"⚠️ Tool use failed, retrying without tools: {e}")
            response = openai_client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            done = True
            break
        
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason == "tool_calls":
            tool_message = response.choices[0].message
            tool_calls = tool_message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(tool_message)
            messages.extend(results)
        else:
            done = True
    
    final_response = response.choices[0].message.content
    
    # Clean any leaked function call text from response
    final_response = clean_response(final_response)
    
    # Cache the response
    set_cached_response(user_query, retrieved_context, final_response)
    
    return final_response
