# import sys

# from app.utils.logger import logger
# from app.utils.exception import StudyAgentException
# from app.ingestion.loader import DocumentLoader
# from app.ingestion.chunker import DocumentChunker
# from app.vector_db.chromadb import ChromaVectorDB
# from app.embedding.embedder import EmbeddingModel
# from app.retrieval.retriever import Retriever
# import sys

# if __name__ == "__main__":
#     try:
#         # documentsLoader = DocumentLoader("data\\raw") 
#         # documents = documentsLoader.load_documents()

#         # print(f"Total Pages : {len(documents)}")
#         # chunker = DocumentChunker()

#         # chunks = chunker.make_chunks(documents)
#         embedding_model = EmbeddingModel()
#         db = ChromaVectorDB(embedding_model=embedding_model.get_embedding_model())

#         # db.add_documents(chunks)

#         retriever = Retriever(
#             vector_db=db,
#             k=3
#         )

#         results = retriever.retrieve(
#             "What is management?"
#         )

#         for i, doc in enumerate(results, start=1):

#             print("=" * 80)
#             print(f"Result {i}")

#             print("Metadata:")
#             print(doc.metadata)

#             print("\nContent:")
#             print(doc.page_content[:500])
#     except Exception as e :
#         raise StudyAgentException(e,sys)
import sys

from app.utils.exception import StudyAgentException

from app.embedding.embedder import EmbeddingModel
from app.vector_db.chromadb import ChromaVectorDB
from app.retriever.retriever import Retriever

from app.rag.llm import GroqLLM
from app.rag.pipeline import RAGPipeline


if __name__ == "__main__":

    try:

        # 1. Create embedding model
        embedding = EmbeddingModel()

        # 2. Connect to existing ChromaDB
        db = ChromaVectorDB(
            embedding_function=embedding.get_embedding_model()
        )

        # 3. Create retriever
        retriever = Retriever(
            vector_db=db,
            k=3
        )

        # 4. Create LLM
        llm = GroqLLM()

        # 5. Create RAG pipeline
        rag = RAGPipeline(
            retriever=retriever,
            llm=llm
        )

        # 6. Ask question
        result = rag.ask(
            "What is the content of the pdf"
        )

        print("\nANSWER")
        print("=" * 80)
        print(result["answer"])

        print("\nSOURCES")
        print("=" * 80)

        for document in result["sources"]:
            print(document.metadata)

    except Exception as e:
        raise StudyAgentException(e, sys)