import fitz  # PyMuPDF

def extract_resume_text(resume_file) -> str:
    """
    Extracts text from a resume PDF using PyMuPDF (fitz).
    """
    try:
        doc = fitz.open(stream=resume_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"
