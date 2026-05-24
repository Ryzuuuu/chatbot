# MemoryBot v0.2 — FastAPI REST Layer

> **Local chatbot with pluggable LangChain memory, now served over HTTP.**  
> Core LLM + memory from v0.1, wrapped in a FastAPI REST API with session management.

---

## What This Version Does

| Capability | Detail |
|------------|--------|
| LLM backend | `Mistral-7B-Instruct-v0.2` via LlamaCpp (GGUF, CPU) or Ollama `mistral` (CPU) |
| Quantization | Q4_K_M — ~4.5GB RAM, full Mistral-7B weights |
| Memory strategies | Buffer · Window · Summary · SummaryBuffer · VectorStore |
| Vector store | ChromaDB with `sentence-transformers/all-MiniLM-L6-v2` embeddings |
| API | FastAPI REST — `/chat`, `/chat/{id}/history`, `/chat/{id}` DELETE |
| Session management | Per-user `ChatbotChain` instances, auto-generated session IDs |
| Interface | HTTP (browser, curl, any client) + Swagger UI at `/docs` |
| Persistence | ChromaDB on local disk (`%USERPROFILE%\chatbot_chroma_db\`) |

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
│   ├── llm_engine.py       ← loads LlamaCpp (GGUF) or Ollama LLM
│   ├── memory.py           ← MemoryFactory (5 memory types)
│   └── chain.py            ← ChatbotChain (wraps LLM + memory + Mistral prompt)
├── models\
│   └── mistral-7b-instruct-v0.2.Q4_K_M.gguf   ← download separately (4.4GB)
├── chatbot-env\            ← Python virtual environment
├── requirements.txt
└── .env
```

---

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11.x | https://python.org/downloads — tick **Add to PATH** |
| Git | Any | https://git-scm.com/download/win |
| VS Code | Any | https://code.visualstudio.com |

> **No GPU required.** Mistral-7B runs fully on CPU via GGUF quantization.  
> Minimum RAM: **14GB total** (close other apps before running).

---

## Installation

```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate

# Install new dependencies (on top of v0.1)
pip install fastapi uvicorn pydantic redis
```

---

## Download the Model

Download the GGUF model file (~4.4GB) and save to `C:\Projects\chatbot\models\`:

```
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

---

## Run

```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate

uvicorn api.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

---

## Test via Swagger UI

Go to `http://127.0.0.1:8000/docs` in your browser.

**Start a conversation:**
1. Open **POST /chat** → Click **Try it out**
2. Send a message (leave `session_id` empty — it auto-generates):
```json
{
  "message": "Hi my name is Neel"
}
```
3. Copy the `session_id` from the response

**Test memory:**
```json
{
  "session_id": "paste-id-here",
  "message": "What is my name?"
}
```
Bot should reply: `Neel`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message, get a reply |
| GET | `/chat/{session_id}/history` | Get full conversation history |
| DELETE | `/chat/{session_id}` | Clear a session |
| GET | `/health` | Health check |

---

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `{"detail":"Not Found"}` at `/` | No root route | Go to `/docs` instead |
| `FileNotFoundError: .gguf not found` | Model not downloaded | Download and place in `models\` |
| Bot adds filler sentences | Prompt behavior | Tighten system prompt in `chain.py` |
| Out of memory crash | Not enough free RAM | Close browser and all apps — need ~5GB free |
| `(chatbot-env)` not in prompt | venv not activated | Run `chatbot-env\Scripts\activate` |

---

## Roadmap

| Version | Focus | Status |
|---------|-------|--------|
| v0.1 | Core LLM + Memory (local console) | ✅ Done |
| **v0.2** | **FastAPI REST layer + session management** | ✅ Done |
| v0.3 | Django web UI + WebSocket streaming | 🔜 Next |
| v0.4 | Image upload + OpenCV + BLIP captioning | — |
| v0.5 | Docker + Docker Compose | — |
| v0.6 | AWS / GCP cloud deployment | — |