# Assignment Requirements Mapping

| Requirement | Implementation |
|---|---|
| Convert unstructured resume/invoice text to JSON | `app/extractor.py`, `app/schemas.py` |
| OpenAI cloud API | Official OpenAI Python SDK; API key loaded from `.env` |
| OpenAI Structured Outputs | `client.beta.chat.completions.parse(..., response_format=ResumeData/InvoiceData)` |
| Pydantic validation | Strict Pydantic v2 models; extra keys forbidden |
| FastAPI | `/extract`, `/health`, `/docs` |
| Empty/invalid input handling | Request validation and explicit empty-text guard |
| API rate-limit/network errors | Helpful messages mapped to HTTP 502 |
| Avoid invented fields | Prompt asks for null/empty lists for missing values; schema validation |
| README and `.env` setup | `README.md`, `.env.example` |
| Tests | `tests/` covers schema and API behavior without calling the real OpenAI API |

## Important limitation
The tests mock the model call, so they do not prove the OpenAI API key, billing, model availability, or live extraction works. Run a live test after configuration.
