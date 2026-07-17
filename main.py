import sys

from app.utils.logger import logger
from app.utils.exception import StudyAgentException
from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import DocumentChunker
from app.vector_db.chromadb import ChromaVectorDB
from app.embedding.embedder import EmbeddingModel
import sys

if __name__ == "__main__":
    try:
        # documentsLoader = DocumentLoader("data\\raw") 
        # documents = documentsLoader.load_documents()

        # print(f"Total Pages : {len(documents)}")
        # chunker = DocumentChunker()

        # chunks = chunker.make_chunks(documents)
        embedding_model = EmbeddingModel()
        db = ChromaVectorDB(embedding_model=embedding_model.get_embedding_model())

        # db.add_documents(chunks)

        results = db.similarity_search(
            "What is management?"
        )

        for i, doc in enumerate(results, start=1):
            print("=" * 80)
            print(f"Result {i}")
            print(doc.metadata)
            print(doc.page_content[:500])
    except Exception as e :
        raise StudyAgentException(e,sys)
