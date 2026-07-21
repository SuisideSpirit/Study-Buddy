from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from app.utils.logger import logger
from app.utils.exception import StudyAgentException
import sys 


class DocumentLoader:

    def __init__(self, data_path: str ):
        self.data_path = (
            Path(data_path)
            if data_path
            else None
        )
        if self.data_path is None:
            raise ValueError("PDF path was not provided")


    def load_pdf(self):

        pdf_path = Path(self.data_path)

        loader = PyMuPDFLoader(str(pdf_path))

        return loader.load()

    def load_file_path(self):
        logger.info(f"started making documents chunks")
        try :
            documents = []

            pdf_files = self.data_path.glob("*.pdf")

            for pdf in pdf_files:
                loader = PyMuPDFLoader(str(pdf))
                documents.extend(loader.load())

            return documents
        except Exception as e :
            raise StudyAgentException(e,sys)
        

    def load_text(self,text: str,source: str = "pasted_text"):

        logger.info(f"Loading pasted text as document. "f"Source: {source}")
        try:

            if not text or not text.strip():
                raise ValueError("No text provided")

            document = Document(page_content=text.strip(),
                metadata={
                    "source": source,
                    "type": "text"
                }
            )
            return [document]

        except Exception as e:
            raise StudyAgentException(e,sys)
        
'''    return Document(
    page_content="Attention Is All You Need...",
    metadata={
        "source": "data/pdfs/transformer.pdf",
        "page": 0
    }
)'''