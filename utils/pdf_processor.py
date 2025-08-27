import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using pdfplumber"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        # st.error() is a UI function, shouldn't be here. Raise exception instead.
        raise Exception(f"Error reading PDF: {str(e)}")

    if not text.strip():
        raise Exception("No text could be extracted from the PDF. The document might be an image-only PDF.")

    return text

def create_text_splitter(chunk_size: int = 1000, chunk_overlap: int = 200):
    """Create a text splitter with specified parameters"""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
