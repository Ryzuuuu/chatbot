# MemoryBot v0.3 — Django Web UI + WebSocket Streaming

> **Full web interface for the chatbot — real-time responses via WebSocket.**  
> FastAPI handles AI inference, Django serves the UI, Redis bridges them with Channels.

---

## What This Version Does

| Capability | Detail |
|------------|--------|
| LLM backend | `Mistral-7B-Instruct-v0.2` via LlamaCpp (GGUF, CPU) |
| Quantization | Q4_K_M — ~4.5GB RAM, full Mistral-7B weights |
| Memory strategies | Buffer · Window · Summary · SummaryBuffer · VectorStore |
| Vector store | ChromaDB with `sentence-transformers/all-MiniLM-L6-v2` embeddings |
| REST API | FastAPI — `/chat`, `/chat/{id}/history`, `/chat/{id}` DELETE |
| Web UI | Django + Channels — real-time chat via WebSocket |
| Session management | Per-user `ChatbotChain` instances, auto-generated session IDs |
| Real-time comms | WebSocket (Daphne + channels-redis) |
| Session persistence | Redis (channels layer + session cache) |

---

## Project Structure

```
C:\Projects\chatbot\
├── api\
│   ├── __init__.py
│   ├── main.py             ← FastAPI app entry point
│   ├── routes.py           ← /chat, /history, /health endpoints
│   └── session_store.py    ← per-user ChatbotChain instances
├── core\
│   ├── __init__.py
│   ├── llm_engine.py       ← LlamaCpp (GGUF) or Ollama
│   ├── memory.py           ← MemoryFactory (5 memory types)
│   └── chain.py            ← ChatbotChain (LLM + memory + Mistral prompt)
├── web_app\                ← auto-created by django-admin
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── chatui\
│   ├── __init__.py
│   ├── consumers.py        ← WebSocket consumer, proxies to FastAPI
│   ├── routing.py          ← WebSocket URL routing
│   ├── urls.py             ← HTTP URL routing
│   ├── views.py            ← chat_view, clear_chat
│   └── templates\
│       └── chatui\
│           └── chat.html   ← full chat UI
├── models\
│   └── mistral-7b-instruct-v0.2.Q4_K_M.gguf
├── chatbot-env\
├── requirements.txt
└── .env
```

---

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11.x | https://python.org/downloads — tick **Add to PATH** |
| Redis | 5.0+ | https://github.com/tporadowski/redis/releases |
| Git | Any | https://git-scm.com/download/win |

> **No GPU required.** Minimum RAM: **14GB total** (close other apps before running).  
> Redis must be 5.0+ — older versions don't support `channels-redis`.

---

## Installation

```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate

pip install django channels channels-redis daphne httpx
```

---

## Download the Model

Download (~4.4GB) and save to `C:\Projects\chatbot\models\`:
```
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

---

## Run — 3 PowerShell Windows

**Window 1 — Redis:**
```powershell
& "C:\Program Files\Redis\redis-server.exe"
```
Verify: `& "C:\Program Files\Redis\redis-cli.exe" ping` → should return `PONG`

**Window 2 — FastAPI:**
```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate
uvicorn api.main:app --reload --port 8000
```

**Window 3 — Django:**
```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate
python manage.py migrate
daphne -b 0.0.0.0 -p 8081 web_app.asgi:application
```

Open `http://localhost:8081`

---

## How It Works

```
Browser (WebSocket)
      ↓
Django + Daphne (port 8081)
      ↓ HTTP POST
FastAPI (port 8000)
      ↓
LangChain Chain + Memory
      ↓
Mistral-7B via LlamaCpp
      ↓
Redis (channels layer, port 6379)
```

Every message goes: browser → Django WebSocket consumer → FastAPI `/chat` → LLM → back through WebSocket to browser.

---

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `unknown command 'BZPOPMIN'` | Redis version too old | Install Redis 5.0+ from tporadowski/redis |
| `WinError 10048` on port 8080 | Port already in use | Use `--port 8081` instead |
| Duplicate welcome messages | WebSocket reconnecting | Remove greeting from `consumers.py` `connect()` |
| Typing indicator stuck, no reply | FastAPI not running | Check uvicorn window for errors |
| `(chatbot-env)` not in prompt | venv not activated | Run `chatbot-env\Scripts\activate` |

---

## Roadmap

| Version | Focus | Status |
|---------|-------|--------|
| v0.1 | Core LLM + Memory (local console) | ✅ Done |
| v0.2 | FastAPI REST layer + session management | ✅ Done |
| **v0.3** | **Django web UI + WebSocket streaming** | ✅ Done |
| v0.4 | Image upload + OpenCV + BLIP captioning | 🔜 Next |
| v0.5 | Docker + Docker Compose | — |
| v0.6 | AWS / GCP cloud deployment | — |