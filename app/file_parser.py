import io

def extract_text_from_file(uploaded_file) -> str:
    """
    Extracts plain text from uploaded .txt, .pdf, or .docx files.
    uploaded_file: Streamlit UploadedFile object
    Returns: extracted text as string
    """
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    # ── Plain Text ──────────────────────────────────────────────────────────
    if filename.endswith(".txt"):
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1")

    # ── PDF ─────────────────────────────────────────────────────────────────
    elif filename.endswith(".pdf"):
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except ImportError:
            return "[Error: PyMuPDF not installed. Run: pip install pymupdf]"
        except Exception as e:
            return f"[PDF parsing error: {str(e)}]"

    # ── DOCX ────────────────────────────────────────────────────────────────
    elif filename.endswith(".docx"):
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)
        except ImportError:
            return "[Error: python-docx not installed. Run: pip install python-docx]"
        except Exception as e:
            return f"[DOCX parsing error: {str(e)}]"

    else:
        return f"[Unsupported file format: {filename}]"
