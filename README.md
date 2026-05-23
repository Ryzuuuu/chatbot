# MemoryBot v0.1 — Core LLM + Memory Engine

> **Local console chatbot with pluggable LangChain memory strategies.**  
> No server, no UI — just pure Python. Build and validate the brain before adding any layers on top.

---

## What This Version Does

| Capability | Detail |
|------------|--------|
| LLM backend | HuggingFace `Mistral-7B-Instruct-v0.2` (GPU) or Ollama `mistral` (CPU) |
| Memory strategies | Buffer · Window · Summary · SummaryBuffer · VectorStore |
| Vector store | ChromaDB with `sentence-transformers/all-MiniLM-L6-v2` embeddings |
| Interface | PowerShell / Command Prompt (REPL loop) |
| Persistence | ChromaDB on local disk (`%USERPROFILE%\chatbot_chroma_db\`) |

---

## Project Structure (this version)

```
C:\Projects\chatbot\
├── core\
│   ├── __init__.py
│   ├── llm_engine.py       ← loads HuggingFace or Ollama LLM
│   ├── memory.py           ← MemoryFactory (5 memory types)
│   └── chain.py            ← ChatbotChain (wraps LLM + memory)
├── chatbot-env\            ← Python virtual environment
├── requirements.txt
└── .env                    ← HF_TOKEN, DJANGO_SECRET_KEY, REDIS_URL
```

---

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11.x | https://python.org/downloads — tick **Add to PATH** |
| Git | Any | https://git-scm.com/download/win |
| VS Code | Any | https://code.visualstudio.com |
| CUDA Toolkit | 12.x | https://developer.nvidia.com/cuda-downloads — **only if NVIDIA GPU** |

> **No GPU?** Use Ollama (free, CPU-friendly). Download: https://ollama.com/download/windows

---

## Installation

Open **PowerShell** and run every command below in order.

```powershell
# 1. Create project root
mkdir C:\Projects\chatbot
cd C:\Projects\chatbot

# 2. Create and activate virtual environment
python -m venv chatbot-env
chatbot-env\Scripts\activate
# Prompt now shows: (chatbot-env) PS C:\Projects\chatbot>

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install langchain langchain-community langchain-core langchain-huggingface transformers torch torchvision sentence-transformers faiss-cpu chromadb python-dotenv
```

> **torch install note:** If the above fails, go to https://pytorch.org/get-started/locally,
> select your OS/CUDA/Python combination, and copy the exact `pip install` command shown.

---

## Configuration

Create and fill `.env` at `C:\Projects\chatbot\.env`:

```env
HF_TOKEN=hf_your_token_here
DJANGO_SECRET_KEY=placeholder_not_used_yet
REDIS_URL=redis://localhost:6379
```

Get your free HuggingFace token at: https://huggingface.co/settings/tokens

---

## Run — Option A: HuggingFace (GPU recommended)

```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate

# Start the REPL chat loop
python core\chain.py
```

Expected output:
```
Loading model mistralai/Mistral-7B-Instruct-v0.2...
You: Hello, my name is Alex
Bot: Hi Alex! Nice to meet you. How can I help you today?

You: What is my name?
Bot: Your name is Alex — you just told me!

You: quit
```

---

## Run — Option B: Ollama (CPU, no GPU needed)

```powershell
# Step 1 — Install Ollama from https://ollama.com/download/windows
# Step 2 — Pull the model (one-time, ~4 GB download)
ollama pull mistral

# Step 3 — Start Ollama server (keep this window open)
ollama serve

# Step 4 — In a NEW PowerShell window, run the bot
cd C:\Projects\chatbot
chatbot-env\Scripts\activate
python -c "
from core.llm_engine import LLMEngine
from core.chain import ChatbotChain

llm = LLMEngine.load_ollama()
bot = ChatbotChain(memory_type='summary_buffer', llm=llm)

while True:
    user = input('You: ')
    if user.lower() == 'quit':
        break
    print(f'Bot: {bot.chat(user)}')
    print()
"
```

---

## Memory Types — Quick Comparison

Switch the `memory_type` argument in `ChatbotChain(memory_type=...)` to try each:

| Type | Argument | Best For | Token Cost |
|------|----------|----------|------------|
| Full buffer | `"buffer"` | Short sessions < 10 turns | High |
| Sliding window | `"window"` | Medium sessions, keeps last 6 turns | Medium |
| Summary | `"summary"` | Long sessions, compresses everything | Low |
| Summary + buffer | `"summary_buffer"` | **Recommended** — balances recall + cost | Low-medium |
| Vector store | `"vector"` | Semantic search over past turns | Very low |

```powershell
# Try a specific memory type
python -c "
from core.chain import ChatbotChain
bot = ChatbotChain(memory_type='window')  # change to: buffer, summary, vector
while True:
    u = input('You: ')
    if u.lower() == 'quit': break
    print(f'Bot: {bot.chat(u)}')
"
```

---

## Verify Imports Work

```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate

python -c "from core.memory import MemoryFactory; print('memory.py OK')"
python -c "from core.chain import ChatbotChain; print('chain.py OK')"
```

Both should print `OK` with no errors.

---

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `'python' is not recognized` | Python not in PATH | Reinstall Python, tick **Add to PATH** |
| `ModuleNotFoundError: langchain` | venv not active | Run `chatbot-env\Scripts\activate` |
| `torch` install hangs or fails | No CUDA match | Use `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `CUDA out of memory` | GPU too small for 7B model | Set `device_map="cpu"` in `llm_engine.py` or switch to Ollama |
| `(chatbot-env)` not in prompt | venv not activated | Run `chatbot-env\Scripts\activate` again |
| ChromaDB permission error | Antivirus blocking | Temporarily disable real-time protection or change `CHROMA_PATH` |

---

## What's Coming Next

| Version | Adds |
|---------|------|
| **v0.2** | FastAPI REST endpoints — chat over HTTP, session IDs, Redis persistence |
| v0.3 | Django web UI with WebSocket streaming |
| v0.4 | Image upload + OpenCV + BLIP captioning |
| v0.5 | Docker + Docker Compose |
| v0.6 | AWS / GCP cloud deployment |