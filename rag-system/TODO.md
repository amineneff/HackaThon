# RAG System TODO

## Setup
- [ ] Add backend and frontend runtime dependencies to `rag-system/requirements.txt` (FastAPI, uvicorn, streamlit, vector DB client, embedding + LLM SDK).
- [ ] Add `.env` support for API keys and model configuration.
- [ ] Add a startup README with local run commands.

## Backend pipeline
- [ ] Finalize Stage 1 in `rag-system/backend/document_processor.py` (chunking strategy + processed text caching).
- [ ] Implement Stage 2 in `rag-system/backend/embedder.py` (provider/model + batching + retries).
- [ ] Implement Stage 3 in `rag-system/backend/vector_store.py` (index creation, upsert, metadata filtering, top-k retrieval).
- [ ] Add a retrieval orchestration layer (query embedding + context assembly).
- [ ] Implement Stage 6 in `rag-system/backend/llm_service.py` (prompt template, source citations, error handling).

## API
- [ ] Build upload endpoint in `rag-system/backend/api.py` that writes files to `rag-system/uploads/`.
- [ ] Build ingest endpoint that processes files and writes cache to `rag-system/processed/`.
- [ ] Build query endpoint that runs retrieval + LLM answer generation.
- [ ] Add request/response schemas and validation.

## Frontend
- [ ] Expand `rag-system/frontend/app.py` with upload flow, ingestion trigger, and chat/query UI.
- [ ] Show retrieved chunks/sources alongside final answer.

## Quality
- [ ] Add unit tests for document processing and vector store adapters.
- [ ] Add API integration tests.
- [ ] Add logging + basic observability (timings, failures, token usage).
- [ ] Add Dockerfile(s) and optional docker-compose for local stack.
