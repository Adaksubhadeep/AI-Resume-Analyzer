import re
from io import BytesIO
from pypdf import PdfReader
from docx import Document

class DocumentParser:
    @staticmethod
    def extract_text(uploaded_file) -> str:
        filename = uploaded_file.name.lower()
        if filename.endswith(".pdf"):
            return DocumentParser._parse_pdf(uploaded_file)
        elif filename.endswith(".docx"):
            return DocumentParser._parse_docx(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

    @staticmethod
    def _parse_pdf(file) -> str:
        try:
            reader = PdfReader(file)
            pages = [page.extract_text() for page in reader.pages if page.extract_text()]
            return DocumentParser.clean_text("\n".join(pages))
        except Exception as e:
            raise RuntimeError(f"Error parsing PDF file: {e}")

    @staticmethod
    def _parse_docx(file) -> str:
        try:
            doc = Document(BytesIO(file.read()))
            text = [p.text for p in doc.paragraphs if p.text]
            return DocumentParser.clean_text("\n".join(text))
        except Exception as e:
            raise RuntimeError(f"Error parsing DOCX file: {e}")

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        return text.strip()