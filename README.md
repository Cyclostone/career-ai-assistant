---
title: Career-AI-Assistant
app_file: app.py
sdk: gradio
sdk_version: 5.49.1
---
# 🤖 Career AI Assistant

An intelligent AI-powered career chatbot with RAG, semantic caching, and an embeddable portfolio widget. Uses Groq's Llama 3.3 70B for blazing-fast, free inference. Deployed on HuggingFace Spaces.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-HuggingFace-blue)](https://huggingface.co/spaces/Cyclostone5945/Career-AI-Assistant)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-green.svg)](https://groq.com/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0+-orange.svg)](https://gradio.app/)

---

## 🌟 Features

- **🧠 RAG Pipeline** - ChromaDB vector database with semantic search for accurate, context-aware responses
- **💰 Semantic Caching** - DiskCache-based caching reduces API calls and costs by serving repeated queries instantly
- **� Embeddable Widget** - Beautiful chat widget with FastAPI backend for portfolio integration
- **�🎯 Personalized Responses** - Trained on LinkedIn profile and career documents
- **📧 Lead Capture** - Automatically records visitor contact information via tool calling
- **💾 Persistent Storage** - SQLite database for leads, knowledge gaps, and cache analytics
- **🔔 Real-time Notifications** - Instant push notifications via Pushover
- **⚡ Blazing Fast** - Powered by Groq's LPU hardware for millisecond inference
- **🆓 Zero API Cost** - Uses Groq's free tier with Llama 3.3 70B model

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              User Interfaces                                  │
│   Gradio Chat UI  │  Embeddable Widget  │  FastAPI Docs      │
└────────┬──────────┴─────────┬───────────┴────────────────────┘
         │                    │
         ▼                    ▼
┌──────────────────────────────────────────────────────────────┐
│                  Core Chat Service                            │
│  • Semantic cache check (DiskCache)                          │
│  • RAG context retrieval (ChromaDB)                          │
│  • Dynamic system prompt construction                        │
│  • Tool calling (lead capture, knowledge gaps)               │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Groq LPU Cloud (via OpenAI-compatible API)       │
│  • Model: llama-3.3-70b-versatile                            │
│  • Function calling enabled                                   │
│  • Free tier - no API costs                                   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  Storage Layer                                 │
│  SQLite (leads, gaps, analytics)  │  DiskCache  │  ChromaDB  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
project_career_ai_assistant/
├── app.py                      # Gradio entry point
├── api_server.py               # FastAPI server for widget
├── config.py                   # Configuration & Groq client
├── requirements.txt            # Python dependencies
├── README.md
├── .env                        # Environment variables (not in repo)
├── .gitignore
│
├── core/                       # Core chat logic
│   ├── __init__.py
│   ├── chat.py                 # Conversation logic with RAG + caching
│   └── tools.py                # AI tool functions (lead capture, etc.)
│
├── rag/                        # RAG pipeline
│   ├── __init__.py
│   ├── vector_store.py         # ChromaDB operations
│   ├── knowledge_indexer.py    # Document chunking & indexing
│   └── retriever.py            # Semantic search retrieval
│
├── storage/                    # Data persistence
│   ├── __init__.py
│   ├── database.py             # SQLite operations
│   └── cache.py                # Semantic caching (DiskCache)
│
├── utils/                      # Utility scripts
│   ├── __init__.py
│   └── view_data.py            # Admin data viewer
│
├── widget/                     # Embeddable portfolio widget
│   └── chat-widget.html        # Standalone chat widget
│
└── data/                       # Runtime data (gitignored)
    ├── knowledge/              # Knowledge base documents
    │   ├── linkedin.pdf
    │   └── summary.txt
    ├── cache/                  # DiskCache storage
    └── chroma_db/              # ChromaDB vector database
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- (Optional) Pushover account for notifications

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Cyclostone/career-ai-assistant.git
   cd career-ai-assistant
   ```

2. **Create virtual environment & install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   GROQ_API_KEY=gsk_your_groq_api_key_here
   PUSHOVER_USER=your-pushover-user-key    # Optional
   PUSHOVER_TOKEN=your-pushover-token      # Optional
   ```

4. **Add your knowledge files**
   
   Place documents in `data/knowledge/`:
   - `linkedin.pdf` - Export your LinkedIn profile as PDF
   - `summary.txt` - Career summary
   - Any `.pdf`, `.txt`, or `.md` files

5. **Index the knowledge base**
   ```bash
   python -m rag.knowledge_indexer
   ```

6. **Run the Gradio app**
   ```bash
   python app.py
   ```
   Open http://127.0.0.1:7860 in your browser

7. **Run the FastAPI server** (for widget)
   ```bash
   python api_server.py
   ```
   API docs at http://127.0.0.1:8000/docs

---

## 🎨 Embeddable Widget

Drop the chat widget into any portfolio website:

1. Start the FastAPI server: `python api_server.py`
2. Open `widget/chat-widget.html` in a browser
3. Update `API_URL` in the widget to point to your deployed server

The widget features:
- Modern UI with typing indicators
- Conversation history
- Error handling with retry
- Fully responsive design

---

## 🛠️ How It Works

### 1. RAG Pipeline
```
User Query → ChromaDB Semantic Search → Top-K Relevant Chunks → Context for LLM
```
- Documents are chunked (500 chars, 50 overlap) and embedded in ChromaDB
- Cosine similarity search retrieves the most relevant context
- Source attribution included in responses

### 2. Semantic Caching
```
User Query → Generate Cache Key → Check DiskCache → HIT: Return cached | MISS: Call LLM
```
- SHA256 hash of query + context as cache key
- 7-day TTL with LRU eviction
- Cache analytics tracked in SQLite

### 3. Conversation Loop
```python
# Check cache first
cached = get_cached_response(query, context)
if cached:
    return cached['response']

# RAG-augmented LLM call
response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools
)
```

### 4. Tool Execution
- **Capture a lead** → `record_user_details(email, name, notes)` → SQLite + Push notification
- **Log unknown question** → `record_unknown_question(question)` → SQLite + Push notification

---

## 📊 Admin Tools

```bash
# View database statistics
python -m utils.view_data stats

# View all captured leads
python -m utils.view_data leads

# View knowledge gaps
python -m utils.view_data gaps

# View cache statistics
python -c "from storage.cache import get_cache_stats; print(get_cache_stats())"

# View cache analytics
python -c "from storage.database import get_cache_analytics; print(get_cache_analytics())"
```

---

## 🔧 Configuration

### Model Settings (`config.py`)

```python
# Groq client (OpenAI-compatible API)
openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"  # Free Groq model
ASSISTANT_NAME = "Arpit Shrotriya"
KNOWLEDGE_DIR = "data/knowledge"
DATABASE_PATH = "data/leads.db"
VECTOR_DB_DIR = "data/chroma_db"
```

---

## 🔐 Security

- API keys stored in environment variables (never committed)
- `.env` file gitignored
- HuggingFace Spaces secrets encrypted
- CORS configured for widget API
- Input validation on all endpoints

---

## 📈 Development Phases

### Phase 1: Core Chat Bot
- Gradio chat interface
- OpenAI GPT-4o-mini integration
- LinkedIn PDF knowledge loading
- Tool calling for lead capture

### Phase 2: Database Integration
- SQLite persistent storage
- Lead management & knowledge gap tracking
- Push notifications via Pushover
- Admin viewer script

### Phase 3: RAG, Caching & Widget (Current)
- ChromaDB vector database with semantic search
- DiskCache semantic caching for cost optimization
- Embeddable portfolio widget with FastAPI backend
- Migration to Groq Llama 3.3 70B (free inference)
- Organized modular codebase

---

## 🤝 Contributing

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
- Powered by [Groq](https://groq.com/), [ChromaDB](https://www.trychroma.com/), [Gradio](https://gradio.app/), and [HuggingFace](https://huggingface.co/)

---

## 📞 Contact

**Arpit Shrotriya**
- 📧 Email: arpit.shrotriya5945@gmail.com
- 🤖 Try the AI: [Career AI Assistant](https://huggingface.co/spaces/Cyclostone5945/Career-AI-Assistant)

---

**Made with ❤️ by Arpit Shrotriya**
