"""FastAPI endpoints for ingestion and RAG querying."""

from fastapi import FastAPI

app = FastAPI(title="RAG System API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
