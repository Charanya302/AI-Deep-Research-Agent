from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_pdf_documents(file_path):

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    loader = PyPDFLoader(str(pdf_path))

    documents = loader.load()

    if not documents:
        raise ValueError("No text found in the PDF.")

    return documents