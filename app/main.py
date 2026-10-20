"""FastAPI service for structured resume and invoice extraction."""

from fastapi import FastAPI, HTTPException
from app.extractor import extract_document
from app.schemas import ExtractionRequest, ExtractionResponse

app = FastAPI(
    title="Data Extraction Bot",
    description="Extract structured resume or invoice data using OpenAI Structured Outputs.",
    version="2.0.0",
)


@app.get("/")
def root():
    return {"name": "Data Extraction Bot", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract", response_model=ExtractionResponse)
def extract(request: ExtractionRequest):
    try:
        data = extract_document(request.text, request.document_type)
        return {"document_type": request.document_type, "data": data}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
