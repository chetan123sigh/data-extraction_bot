import pytest
from pydantic import ValidationError

from app.schemas import ExtractionRequest, ExtractionType, InvoiceData, ResumeData


def test_request_rejects_empty_text():
    with pytest.raises(ValidationError):
        ExtractionRequest(text="   ", document_type=ExtractionType.RESUME)


def test_request_rejects_extra_fields():
    with pytest.raises(ValidationError):
        ExtractionRequest(text="Resume", document_type="resume", extra="no")


def test_resume_schema_accepts_null_missing_fields():
    item = ResumeData(
        full_name=None, email=None, phone=None, location=None, summary=None,
        skills=[], education=[], experience=[]
    )
    assert item.full_name is None


def test_invoice_schema_accepts_null_amounts():
    item = InvoiceData(
        invoice_number=None, invoice_date=None, due_date=None, vendor=None,
        customer=None, currency=None, subtotal=None, tax=None, total=None,
        line_items=[]
    )
    assert item.total is None


def test_schemas_forbid_extra_fields():
    with pytest.raises(ValidationError):
        ResumeData(
            full_name=None, email=None, phone=None, location=None, summary=None,
            skills=[], education=[], experience=[], invented="x"
        )
