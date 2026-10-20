"""Streamlit UI for the Data Extraction Bot."""

import io
import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from docx import Document
from pypdf import PdfReader

load_dotenv()
API_URL = os.getenv("EXTRACTION_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Data Extraction Bot", page_icon="📄", layout="centered")
st.title("📄 Data Extraction Bot")
st.caption("Turn resume or invoice text into validated JSON using OpenAI Structured Outputs.")


def read_upload(uploaded_file) -> str:
    suffix = uploaded_file.name.lower().rsplit(".", 1)[-1]
    raw = uploaded_file.getvalue()
    if suffix == "txt":
        return raw.decode("utf-8", errors="replace")
    if suffix == "pdf":
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == "docx":
        document = Document(io.BytesIO(raw))
        return "\n".join(p.text for p in document.paragraphs)
    raise ValueError("Unsupported file type.")


kind = st.selectbox("Document type", ["resume", "invoice"])
uploaded = st.file_uploader("Upload a TXT, text-based PDF, or DOCX (optional)", type=["txt", "pdf", "docx"])
default_text = ""
if uploaded:
    try:
        default_text = read_upload(uploaded)
        if not default_text.strip():
            st.warning("No text was found. Scanned PDFs need OCR before extraction.")
    except Exception as exc:
        st.error(f"Could not read file: {exc}")

text_input = st.text_area("Or paste document text", value=default_text, height=240, max_chars=50000)
if st.button("Extract structured data", type="primary", disabled=not text_input.strip()):
    try:
        with st.spinner("Extracting with OpenAI..."):
            response = requests.post(
                f"{API_URL.rstrip('/')}/extract",
                json={"document_type": kind, "text": text_input},
                timeout=90,
            )
        if response.ok:
            result = response.json()
            st.success("Extraction completed.")
            st.json(result)
            st.download_button(
                "Download JSON",
                data=json.dumps(result, indent=2, ensure_ascii=False),
                file_name=f"{kind}_extraction.json",
                mime="application/json",
            )
        else:
            detail = response.json().get("detail", response.text)
            st.error(f"API error ({response.status_code}): {detail}")
    except requests.RequestException as exc:
        st.error(f"Cannot reach the FastAPI server at {API_URL}. Start it first. Details: {exc}")
