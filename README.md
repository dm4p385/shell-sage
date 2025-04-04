# 🤖 ShellSage

> ✨ Context-aware, low-latency command-line autocomplete powered by Trie, FAISS, and LLMs.

ShellSage is my attempt at an intelligent autocomplete engine for your terminal that combines the speed of Trie-based search, the semantic understanding of FAISS, and the reasoning capabilities of LLMs to provide blazing-fast, contextually relevant command suggestions.
> NOTE: This is only supported in fish at the moment
---

## 🚀 Features

- ⚡ **Low-latency Suggestions** using Trie prefix search  
- 🧠 **Context-aware Search** using FAISS semantic embeddings  
- 🤖 **LLM-Powered Completions** to refine and personalize suggestions  
- 📚 **User Command History Integration**  
- 📃️ **Hybrid Ranking Engine** combining all sources  
- 🧵 **gRPC-based Streaming API** for interactive clients  
- 💾 **FAISS Cache** to reuse LLM results and reduce API latency  
- 🔐 **Modular, extensible engine** built in Python

---

## 🏗️ Architecture

```
                 ┌─────────────┐
                 │   Terminal  │
                 └─────────────┘
                        │
               gRPC backend client
                        │
              ┌───────────────────┐
              │   ShellSage Core  │
              └───────────────────┘
   ┌────────────────────│──────────────────────┐
   │             │              │              │
TrieSearch   FaissSearch   LLMCompletion   FaissCache
(prefix)     (semantic)     (GPT-like)     (embedding cache)
```

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/shellsage.git
cd shellsage

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install ollama
<install ollama>

# Pull mistral
ollama pull mistral
```

---

## 🥪 Running the Server

```bash
python -m src.api.server
```

This will start the **gRPC server** on `localhost:50051`. It uses a thread pool executor and gracefully handles streamed prompts from clients.

---

## 🧠 Core Components

| Component         | Description                                |
|------------------|--------------------------------------------|
| `TrieSearch`      | Fast prefix matching from shell history    |
| `FaissSearch`     | Vector search using sentence embeddings    |
| `LLMCompletion`   | Calls local AI model to refine suggestions |
| `FaissCache`      | Embedding-keyed cache to avoid redundant LLM calls |
| `Ranker`          | Combines and scores all results            |
| `gRPC Server`     | Streams back autocomplete results to clients |

---


## 📁 Project Structure

```
src/
├── api/                 # gRPC server & protobufs
├── prediction_engine/   # Core engine components
│   ├── core/            # Trie, FAISS, LLM logic
│   ├── data/            # History loader
│   └── ranking/         # Result ranking strategy
├── utils/               # Logging, helpers
├── protobuf/            # Generated gRPC code
```

---

## 📝 TODO

- [ ] Shell plugin for Bash/Zsh/Fish autocompletion
- [ ] Persistent command history across sessions
- [ ] Create a proper RAG for LLM (might increase latency)
- [ ] Session-aware completions

---


## 📄 License

MIT License © 2025 Harsh S.

