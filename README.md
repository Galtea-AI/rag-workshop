# 🧠 Retrieval-Augmented Generation (RAG) Workshop

Welcome! This workshop will teach you the basics of Retrieval-Augmented Generation (RAG) using Python and LangChain, and a local chromadb vector store. By the end, you'll build and test your own document-aware chatbot.

## 🚀 Quickstart

1. **Clone the repo**
   ```bash
   git clone https://github.com/galtea/rag-workshop.git
   cd rag-workshop
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your `.env`**
   ```bash
   cp .env.example .env
   ```
   Add your OpenAI.

4. **Create a vector database from a text file**
   ```bash
   python utils/create_vector_database.py --chunk_size 1024 --chunk_overlap 256
   ```

5. **Run a working RAG pipeline**
   ```bash
   python rag/run_rag.py --query "<query>" --threshold 0.7
   ```

6. **Deploy as an API**
   ```bash
   uvicorn app.main:app --reload
   ```
   You can launch the queries via `curl`, `postman` or from http://127.0.0.1:8000/docs


7. **Start exploring!**
   - Tune the prompt: `rag/prompt_template.txt`
   - Modify chunking logic: `utils/create_vector_database.py`
   - Add your own documents to `docs/`

---

## 📂 Folders Explained

- `ingestion/`: Load and chunk documents
- `vector_store/`: Build and save your vector index
- `rag/`: Combine retrieval + generation
- `evaluation/`: Manually or automatically evaluate responses
- `utils/`: API wrappers and helper functions

---

## 🧠 Concepts Covered

- Vector embeddings and similarity search
- Prompt engineering
- Retrieval-Augmented Generation (RAG) architecture
- Evaluation of LLM-based systems

---

## 📌 Requirements

- Python 3.9+
- API access to an LLM provider (e.g., OpenAI, AWS Bedrock)

---

## 🙌 Credits

Created by Galtea.
