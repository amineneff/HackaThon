# ml_pipeline_integration.py

from document_processor import DocumentProcessor
import json

class DocumentIngestionPipeline:
    """Integration with ML/AI pipeline"""
    
    def __init__(self):
        self.processor = DocumentProcessor(
            whisper_model="base",
            ocr_language="eng"
        )
    
    def ingest_and_prepare(self, file_path: str) -> dict:
        """
        Process document and prepare for ML pipeline.
        
        Returns structured data ready for:
        - Vector embedding
        - LLM processing
        - Feature extraction
        """
        result = self.processor.process_document(file_path)
        
        if not result.success:
            raise ValueError(f"Processing failed: {result.error_message}")
        
        return {
            "document_id": hash(file_path),
            "source_path": result.file_path,
            "source_type": result.document_type.value,
            "raw_text": result.raw_text,
            "metadata": {
                **result.metadata,
                "processing_timestamp": "2025-02-14T10:30:00Z"
            },
            # Ready for downstream ML tasks
            "ready_for_embedding": True,
            "ready_for_llm": True
        }
    
    def save_processed_output(self, file_path: str, output_path: str):
        """Save processed text to JSON for downstream consumption"""
        data = self.ingest_and_prepare(file_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved processed document to {output_path}")


# Usage in ML pipeline
if __name__ == "__main__":
    pipeline = DocumentIngestionPipeline()
    
    # Process and save
    pipeline.save_processed_output(
        "input/research_paper.pdf",
        "output/processed/research_paper.json"
    )
    