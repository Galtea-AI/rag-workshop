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

## 🐳 Docker

Build the Docker image:
```bash
docker build -t galtea/rag-workshop .
```

Create a vector database:
```bash
docker run --rm \
  --env-file .env \
  --volume ./chroma:/app/chroma \
  galtea/rag-workshop \
  python utils/create_vector_database.py --chunk_size 1024 --chunk_overlap 256
```

Run the RAG pipeline:
```bash
docker run --rm \
  --env-file .env \
  --volume ./chroma:/app/chroma \
  galtea/rag-workshop \
  python rag/run_rag.py --query "<query>" --threshold 0.7
```

Run the API:
```bash
docker run --rm \
  --env-file .env \
  --volume ./chroma:/app/chroma \
  -p 8000:8000 \
  galtea/rag-workshop \
  uvicorn app.main:app --host 0.0.0.0 --reload --port 8000
```


## 📌 Requirements

- Python 3.10+
- API access to an LLM provider (OpenAI)

---

## 🙌 Credits

Created by Galtea.
