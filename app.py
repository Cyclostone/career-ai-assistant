"""
Gradio app - the main entry point.
"""

import gradio as gr
from chat import chat

# Launch Gradio interface
if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch()