"""Pydantic schemas used for strict OpenAI Structured Outputs."""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class ExtractionType(str, Enum):
    RESUME = "resume"
    INVOICE = "invoice"


class ExtractionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=50_000)
    document_type: ExtractionType


class StrictSchema(BaseModel):
    """Base schema configured to reject undeclared keys."""
    model_config = ConfigDict(extra="forbid")


class EducationItem(StrictSchema):
    qualification: str | None
    institution: str | None
    graduation_year: str | None
    details: str | None


class ExperienceItem(StrictSchema):
    job_title: str | None
    company: str | None
    start_date: str | None
    end_date: str | None
    description: str | None


class ResumeData(StrictSchema):
    full_name: str | None
    email: str | None
    phone: str | None
    location: str | None
    summary: str | None
    skills: list[str]
    education: list[EducationItem]
    experience: list[ExperienceItem]


class InvoiceLineItem(StrictSchema):
    description: str | None
    quantity: float | None
    unit_price: float | None
    amount: float | None


class InvoiceData(StrictSchema):
    invoice_number: str | None
    invoice_date: str | None
    due_date: str | None
    vendor: str | None
    customer: str | None
    currency: str | None
    subtotal: float | None
    tax: float | None
    total: float | None
    line_items: list[InvoiceLineItem]


class ExtractionResponse(StrictSchema):
    document_type: ExtractionType
    data: ResumeData | InvoiceData
