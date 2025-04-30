build:
	docker build -t galtea/rag-workshop .

run-api:
	docker run --rm \
		--env-file .env \
		--volume ./chroma:/app/chroma \
		-p 8000:8000 \
		galtea/rag-workshop uvicorn app.main:app --host 0.0.0.0 --reload --port 8000