from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader

class DocumentLoader:

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_documents(self):
        documents = []

        pdf_files = self.data_path.glob("*.pdf")

        for pdf in pdf_files:
            loader = PyMuPDFLoader(str(pdf))
            documents.extend(loader.load())

        return documents
    
'''    return Document(
    page_content="Attention Is All You Need...",
    metadata={
        "source": "data/pdfs/transformer.pdf",
        "page": 0
    }
)'''