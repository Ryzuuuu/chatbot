# MemoryBot v0.1 — Core LLM + Memory Engine

> **Local console chatbot with pluggable LangChain memory strategies.**  
> No server, no UI — just pure Python. Build and validate the brain before adding any layers on top.

---

## What This Version Does

| Capability | Detail |
|------------|--------|
| LLM backend | `Mistral-7B-Instruct-v0.2` via LlamaCpp (GGUF, CPU) or Ollama `mistral` (CPU) |
| Quantization | Q4_K_M — ~4.5GB RAM, full Mistral-7B weights |
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
│   ├── llm_engine.py       ← loads LlamaCpp (GGUF) or Ollama LLM
│   ├── memory.py           ← MemoryFactory (5 memory types)
│   └── chain.py            ← ChatbotChain (wraps LLM + memory + Mistral prompt)
├── models\
│   └── mistral-7b-instruct-v0.2.Q4_K_M.gguf   ← download separately (4.4GB)
├── chatbot-env\            ← Python virtual environment
├── requirements.txt
└── .env                    ← DJANGO_SECRET_KEY, REDIS_URL (HF_TOKEN no longer needed)
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
pip install llama-cpp-python langchain-community langchain-core langchain-huggingface sentence-transformers chromadb python-dotenv
```

---

## Download the Model

Download the GGUF model file (~4.4GB) in your browser and save to `C:\Projects\chatbot\models\`:

```
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

Create the folder first if it doesn't exist:

```powershell
mkdir C:\Projects\chatbot\models
```

---

## Configuration

Create `.env` at `C:\Projects\chatbot\.env`:

```env
DJANGO_SECRET_KEY=placeholder_not_used_yet
REDIS_URL=redis://localhost:6379
```

> `HF_TOKEN` is no longer needed — the model runs from the local GGUF file.

---

## Run

```powershell
cd C:\Projects\chatbot
chatbot-env\Scripts\activate

python core\chain.py
```

Expected output:
```
Loading model mistralai/Mistral-7B-Instruct-v0.2...
Loading model from C:\Projects\chatbot\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf...
You: Hello, my name is Alex
Bot: Hi Alex! Nice to meet you. How can I help you today?

You: What is my name?
Bot: Your name is Alex.

You: quit
```

---

## Run — Option B: Ollama (alternative CPU option)

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
| `FileNotFoundError: .gguf not found` | Model not downloaded | Download the `.gguf` file and place in `models\` |
| `RuntimeWarning: duplicate leading <s>` | Old prompt template | LlamaCpp adds `<s>` automatically — do not include it in the template |
| Bot continues conversation on its own | Missing stop tokens | Ensure `stop=["Human:", "\nHuman:"]` is set in `LlamaCpp(...)` |
| `(chatbot-env)` not in prompt | venv not activated | Run `chatbot-env\Scripts\activate` again |
| ChromaDB permission error | Antivirus blocking | Temporarily disable real-time protection or change `CHROMA_PATH` |
| Out of memory crash | Not enough free RAM | Close browser and all apps — need ~5GB free |

---

## What's Coming Next

| Version | Adds |
|---------|------|
| **v0.2** | FastAPI REST endpoints — chat over HTTP, session IDs, Redis persistence |
| v0.3 | Django web UI with WebSocket streaming |
| v0.4 | Image upload + OpenCV + BLIP captioning |
| v0.5 | Docker + Docker Compose |
| v0.6 | AWS / GCP cloud deployment |