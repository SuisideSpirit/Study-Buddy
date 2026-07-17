import sys

from app.utils.logger import logger
from app.utils.exception import StudyAgentException
from app.ingestion.loader import DocumentLoader
from app.chunking.chunker import DocumentChunker
import sys

if __name__ == "__main__":
    try:
        documentsLoader = DocumentLoader("data\\raw") 
        documents = documentsLoader.load_documents()

        print(f"Total Pages : {len(documents)}")
        chunker = DocumentChunker()

        chunks = chunker.make_chunks(documents)

        print(f"Pages : {len(documents)}")

        print(f"Chunks : {len(chunks)}")

        print(chunks[1].metadata)

        print(chunks[1].page_content)

    except Exception as e :
        raise StudyAgentException(e,sys)