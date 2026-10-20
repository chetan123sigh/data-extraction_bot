# Data Extraction Bot — OpenAI Structured Outputs

A small Python project that extracts structured **resume** or **invoice** data from unstructured text. It uses the **actual OpenAI cloud API**, OpenAI Structured Outputs, Pydantic v2, and FastAPI. A Streamlit UI supports pasted text and TXT, text-based PDF, and DOCX uploads.

> **API costs:** This project sends document text to OpenAI. You need an OpenAI API key and an API project with available quota/billing. API usage may incur charges. ChatGPT subscriptions and API billing are separate.

## Features

- Resume and invoice extraction into typed JSON
- OpenAI Structured Outputs through Pydantic response models
- Missing scalar fields represented as `null`; missing collections as `[]`
- Strict schemas reject undeclared fields
- FastAPI validation and `/docs` Swagger UI
- Streamlit interface with JSON download
- Friendly handling of missing API key, rate limits, timeouts, and API errors
- Unit/API tests that mock model calls

## Requirements

- Python 3.10+
- Internet access
- An OpenAI API key with API access and quota
- Windows 11, macOS, or Linux

## Setup — Windows Git Bash

Run commands from the extracted project directory:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and replace `your_openai_api_key_here` with your real key:

```dotenv
OPENAI_API_KEY=sk-your-real-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_TIMEOUT_SECONDS=60
```

Keep `.env` private. Never commit it or paste your API key into chat. `gpt-4o-mini` supports Structured Outputs. You can change the model to another compatible model available to your API project.

## Run the API

In terminal 1, with the virtual environment activated:

```bash
uvicorn app.main:app --reload
```

Check:
- API home: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs

## Run the Streamlit UI

Open terminal 2 in the same project directory and activate the environment:

```bash
source .venv/Scripts/activate
python -m streamlit run streamlit_app.py
```

Paste text or upload a TXT, text-based PDF, or DOCX file, choose resume/invoice, and click **Extract structured data**. Scanned PDFs need OCR first.

## Test with curl

```bash
curl -X POST http://127.0.0.1:8000/extract -H "Content-Type: application/json" -d '{"document_type":"resume","text":"Asha Rao, Jaipur. Email: asha@example.com. Skills: Python, FastAPI."}'
```

The response has a `document_type` and `data` object. Exact extracted values depend on the document supplied.

## Run tests

```bash
python -m pytest -v
```

Tests use mocked extraction results; they do not require a live API key and do not test live model accuracy.

## Troubleshooting

- **Missing API key:** check `.env` exists in the project root and `OPENAI_API_KEY` is set.
- **401 authentication error:** verify the key and that it is active.
- **429 rate limit/quota:** check the API project's limits and billing; wait and retry if rate-limited.
- **Model not found / unsupported model:** set `OPENAI_MODEL` to a model available to your API project that supports Structured Outputs.
- **Connection/time-out:** check internet and retry.
- **No text from PDF:** scanned/image-only PDFs require OCR; this app extracts embedded text only.
- **Import/module errors:** activate the project `.venv` and run commands from the project root.

## Project structure

```text
data-extraction-bot/
├── app/
│   ├── __init__.py
│   ├── schemas.py
│   ├── extractor.py
│   └── main.py
├── tests/
│   ├── test_schemas.py
│   └── test_api.py
├── docs/
│   └── ASSIGNMENT_REQUIREMENTS.md
├── .env.example
├── .gitignore
├── requirements.txt
├── streamlit_app.py
└── README.md
```

## How Structured Outputs works

1. Pydantic models define the allowed fields and types.
2. The OpenAI SDK sends the model schema using `response_format`.
3. OpenAI constrains the response to the schema, when supported by the selected model.
4. The SDK parses the response into the Pydantic model.
5. The API returns the validated data as JSON.

## Security and privacy notes

- Uploaded/pasted document text is sent to the OpenAI API for processing.
- Do not use real sensitive resumes or invoices unless you are authorized to process and share them with the configured service.
- `.env` is excluded from Git by `.gitignore`.
- The prompt treats document text as untrusted content and tells the model not to follow instructions inside it. This is a mitigation, not a guarantee against every prompt-injection attempt.

## Scope and limitations

- Supports resumes and invoices only.
- This is an extraction aid, not a source of truth; manually verify financial totals and personal details.
- Numeric invoice amounts use floating-point fields for simplicity; financial-grade systems should use decimal arithmetic.
- No OCR, database, authentication, or production deployment is included.
