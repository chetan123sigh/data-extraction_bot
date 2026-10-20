from fastapi.testclient import TestClient
from app.main import app
import app.main as main_module

client = TestClient(app)


def test_root_and_health():
    assert client.get("/").status_code == 200
    assert client.get("/health").json() == {"status": "ok"}


def test_blank_text_is_rejected():
    response = client.post("/extract", json={"document_type": "resume", "text": ""})
    assert response.status_code == 422


def test_successful_extract(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "extract_document",
        lambda text, document_type: {
            "full_name": "Asha Rao", "email": None, "phone": None, "location": None,
            "summary": None, "skills": [], "education": [], "experience": []
        },
    )
    response = client.post(
        "/extract",
        json={"document_type": "resume", "text": "Asha Rao, Python developer"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == "Asha Rao"


def test_runtime_error_maps_to_502(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("OpenAI unavailable")
    monkeypatch.setattr(main_module, "extract_document", fail)
    response = client.post(
        "/extract", json={"document_type": "resume", "text": "Some resume text"}
    )
    assert response.status_code == 502
    assert "OpenAI unavailable" in response.json()["detail"]
