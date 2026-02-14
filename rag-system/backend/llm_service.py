"""LLM utilities for document transformation and RAG answering."""

import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


class LLMService:
    """Thin wrapper over an LLM provider (OpenAI) for this project."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.model = model
        self.temperature = temperature
        self._client: Optional[OpenAI] = None

    def _get_client(self) -> OpenAI:
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY is not set")
            self._client = OpenAI(api_key=api_key)
        return self._client

    def transform_document(
        self,
        raw_text: str,
        metadata: Optional[Dict[str, Any]] = None,
        instruction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Use LLM to normalize and structure extracted document text."""
        if not raw_text or not raw_text.strip():
            return {
                "cleaned_text": "",
                "summary": "",
                "key_points": [],
                "topics": [],
            }

        instruction_text = instruction or "Clean noisy extraction output and preserve meaning."
        metadata = metadata or {}

        system_prompt = (
            "You are a document normalization engine for a RAG pipeline. "
            "Return valid JSON only."
        )
        user_prompt = (
            "Given extracted document text and metadata, produce JSON with keys: "
            "cleaned_text (string), summary (string), key_points (array of strings), "
            "topics (array of strings).\n\n"
            f"Instruction: {instruction_text}\n"
            f"Metadata: {json.dumps(metadata, ensure_ascii=True)}\n\n"
            f"Raw text:\n{raw_text}"
        )

        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content or "{}"
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {
                "cleaned_text": raw_text,
                "summary": content.strip(),
                "key_points": [],
                "topics": [],
            }

        parsed.setdefault("cleaned_text", raw_text)
        parsed.setdefault("summary", "")
        parsed.setdefault("key_points", [])
        parsed.setdefault("topics", [])
        return parsed

    def answer_query(self, question: str, context_chunks: List[str]) -> str:
        """Generate a grounded answer from retrieved context chunks."""
        joined_context = "\n\n".join(context_chunks)
        prompt = (
            "Answer using only the provided context. If context is insufficient, say so.\n\n"
            f"Question: {question}\n\n"
            f"Context:\n{joined_context}"
        )

        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return (response.choices[0].message.content or "").strip()


def answer_query(question: str, context_chunks: List[str]) -> str:
    """Backward-compatible function entrypoint."""
    service = LLMService()
    return service.answer_query(question=question, context_chunks=context_chunks)
