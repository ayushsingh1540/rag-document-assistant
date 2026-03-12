# Enterprise RAG Assistant

A Retrieval-Augmented Generation (RAG) system built using FastAPI, FAISS, SentenceTransformers, and Ollama.

This system allows users to query documents and receive context-aware answers powered by local LLMs.

---

## Features

- Semantic document search using FAISS
- Local LLM inference using Ollama
- FastAPI backend for API access
- Streamlit UI for chat interface
- Conversation memory support
- SQLite metadata storage

---

## Architecture

User → Streamlit UI → FastAPI → Query Engine → FAISS Vector DB → Ollama LLM

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/rag-assistant.git
cd rag-assistant

Create virtual environment:

python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Place your documents inside:

data/raw_docs/

Then run:

python src/build_index.py

Run Backend :

uvicorn src.api:app --reload

Run UI :

streamlit run ui/ui.py

--------------------------------------------------------------------