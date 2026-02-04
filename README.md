---
title: Career-AI-Assistant
app_file: app.py
sdk: gradio
sdk_version: 5.49.1
---
# 🤖 Career AI Assistant

An intelligent AI-powered chatbot that acts as your professional alter-ego, answering questions about your career, background, and skills on your website. Built with OpenAI's GPT-4 and deployed on HuggingFace Spaces.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-HuggingFace-blue)](https://huggingface.co/spaces/Cyclostone5945/Career-AI-Assistant)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0+-orange.svg)](https://gradio.app/)

---

## 🌟 Features

- **🎯 Personalized Responses** - Trained on your LinkedIn profile and career summary to answer questions authentically
- **📧 Lead Capture** - Automatically records visitor contact information when they express interest
- **� Persistent Storage** - SQLite database ensures no lead is ever lost (Phase 2)
- **�📊 Knowledge Gap Tracking** - Logs unanswered questions to help improve your knowledge base
- **🔔 Real-time Notifications** - Instant push notifications via Pushover when leads are captured
- **📈 Analytics Ready** - View historical data and statistics with built-in admin tools
- **⚡ Fast & Scalable** - Deployed on HuggingFace Spaces with automatic scaling
- **🛠️ Tool Use** - Leverages OpenAI's function calling for intelligent action execution

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│                  (Gradio Chat Widget)                   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                  Chat Service (chat.py)                 │
│  • Loads knowledge (LinkedIn PDF + Summary)             │
│  • Builds system prompt with context                    │
│  • Manages conversation loop                            │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              OpenAI GPT-4 (via config.py)               │
│  • Model: gpt-4o-mini                                   │
│  • Function calling enabled                             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                  Tools (tools.py)                       │
│  • record_user_details() - Capture leads                │
│  • record_unknown_question() - Track knowledge gaps     │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│            Database (database.py) + Pushover            │
│  • SQLite for permanent storage                         │
│  • Push notifications for real-time alerts              │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
project_career_ai_assistant/
├── app.py                  # Gradio entry point
├── config.py               # Configuration & OpenAI client
├── chat.py                 # Main conversation logic
├── tools.py                # AI tool functions
├── database.py             # Database operations (SQLite)
├── view_data.py            # Admin script to view stored data
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
├── data/
│   ├── knowledge/
│   │   ├── linkedin.pdf    # Your LinkedIn profile
│   │   └── summary.txt     # Career summary
│   └── leads.db            # SQLite database (auto-created)
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key
- (Optional) Pushover account for notifications

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/career-ai-assistant.git
   cd career-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here
   PUSHOVER_USER=your-pushover-user-key  # Optional
   PUSHOVER_TOKEN=your-pushover-token    # Optional
   ```

4. **Add your knowledge files**
   
   Place these files in `data/knowledge/`:
   - `linkedin.pdf` - Export your LinkedIn profile as PDF
   - `summary.txt` - Write a brief career summary

5. **Run locally**
   ```bash
   python app.py
   ```
   
   Open http://127.0.0.1:7860 in your browser

---

## 🌐 Deployment

### HuggingFace Spaces (Recommended)

1. **Install HuggingFace CLI**
   ```bash
   uv tool install 'huggingface_hub[cli]'
   hf auth login --token YOUR_HF_TOKEN
   ```

2. **Deploy**
   ```bash
   uv run gradio deploy
   ```

3. **Configure secrets in HuggingFace**
   - `OPENAI_API_KEY`
   - `PUSHOVER_USER` (optional)
   - `PUSHOVER_TOKEN` (optional)

Your Space will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/career-ai-assistant`

---

## 🛠️ How It Works

### 1. Knowledge Loading
The system loads your professional background from:
- **LinkedIn PDF** - Parsed using `pypdf` library
- **Summary text** - Plain text career overview

### 2. System Prompt Construction
A dynamic prompt is built that:
- Instructs the AI to act as you
- Includes your background context
- Defines tool usage guidelines
- Sets professional tone

### 3. Conversation Loop
```python
while not done:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools  # Available functions
    )
    
    if finish_reason == "tool_calls":
        # Execute tools (e.g., record_user_details)
        results = handle_tool_calls(tool_calls)
        messages.extend(results)
    else:
        done = True  # Return final response
```

### 4. Tool Execution
When the AI needs to:
- **Capture a lead** → Calls `record_user_details(email, name, notes)`
- **Log unknown question** → Calls `record_unknown_question(question)`

Both save to database first (permanent storage), then send push notifications via Pushover.

---

## � Database & Lead Management (Phase 2)

### Persistent Storage

All leads and knowledge gaps are now permanently stored in a SQLite database (`data/leads.db`):

**Tables:**
- `leads` - Contact information with timestamps
- `knowledge_gaps` - Unanswered questions for improvement
- `conversations` - Full conversation history (future use)

### Viewing Your Data

Use the included admin script to view stored data:

```bash
# View statistics
python view_data.py stats

# View all leads
python view_data.py leads

# View knowledge gaps
python view_data.py gaps
```

**Example Output:**
```
📊 Database Statistics
==================================================
Total Leads: 15
Total Knowledge Gaps: 3
==================================================
```

### Data Flow

```
User provides email → Save to Database (permanent) → Send Pushover notification
```

**Benefits:**
- ✅ Never lose leads even if notifications fail
- ✅ Historical data for analytics
- ✅ Track which questions need better answers
- ✅ Foundation for future CRM integration

---

## �🔧 Configuration

### Model Settings (`config.py`)

```python
MODEL = "gpt-4o-mini"           # OpenAI model
ASSISTANT_NAME = "Your Name"    # Your identity
KNOWLEDGE_DIR = "data/knowledge" # Knowledge base path
DATABASE_PATH = "data/leads.db" # SQLite database path
```

### Tool Schemas (`tools.py`)

Tools are defined with OpenAI function calling format:
```python
{
    "name": "record_user_details",
    "description": "Use this tool to record...",
    "parameters": {
        "type": "object",
        "properties": {...},
        "required": ["email"]
    }
}
```

---

## 📊 Usage Examples

### Example Conversation

**User:** "What's your experience with Python?"

**AI:** "I have extensive experience with Python, particularly in AI/ML development. I've worked on projects involving OpenAI's GPT models, built conversational agents, and deployed applications on cloud platforms..."

**User:** "I'd love to discuss a project. My email is john@example.com"

**AI:** "Thank you, John! I've recorded your information and will reach out soon."

*→ Lead saved to database (ID: 42)*  
*→ Push notification sent: "Recording interest from John with email john@example.com"*

---

## 🔐 Security

- ✅ API keys stored in environment variables (never committed)
- ✅ `.env` file gitignored
- ✅ HuggingFace Spaces secrets encrypted
- ✅ Input validation on tool parameters

---

## 📈 Future Enhancements

### ✅ Phase 2: Database Integration (COMPLETED)

- ✅ SQLite database for lead persistence
- ✅ Admin viewer script (`view_data.py`)
- ✅ Knowledge gap tracking
- ✅ Conversation history foundation

### Planned Improvements (Phase 3+)

1. **🧠 RAG (Retrieval-Augmented Generation)**
   - ChromaDB vector store for better knowledge retrieval
   - Semantic search over documents
   - Source attribution in responses

2. **💰 Cost Optimization**
   - Semantic caching (Redis) for common questions
   - Model routing (cheap vs. expensive models)
   - Token usage monitoring

3. **📧 Enhanced Notifications**
   - Email via AWS SES/SendGrid
   - Slack/Discord webhooks
   - Batched daily digests

4. **🎨 Enhanced UI**
   - Custom Gradio theme
   - Embedded widget for portfolio website
   - Mobile-responsive design

5. **🔌 Portfolio Integration**
   - FastAPI backend for external calls
   - Embeddable JavaScript widget
   - Session tracking and analytics

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built as part of the [Agentic AI Course](https://github.com/ed-donner/agents)
- Inspired by Ed Donner's Lab 4 - Career Conversation project
- Powered by [OpenAI](https://openai.com/), [Gradio](https://gradio.app/), and [HuggingFace](https://huggingface.co/)

---

## 📞 Contact

**Arpit Shrotriya**
- 🌐 Portfolio: [Your Website]
- 💼 LinkedIn: [Your LinkedIn]
- 📧 Email: arpit.shrotriya5945@gmail.com
- 🤖 Try the AI: [Career AI Assistant](https://huggingface.co/spaces/Cyclostone5945/Career-AI-Assistant)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by Arpit Shrotriya**
Testing Huggingface and Github Sync
