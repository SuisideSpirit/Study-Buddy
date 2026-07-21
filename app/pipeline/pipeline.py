from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import DocumentChunker
from app.vector_db.chromadb import ChromaVectorDB
from app.retriever.retriever import Retriever
from app.rag.llm import GroqLLM
from app.memory.memory import StudyBuddyMemory
from app.prompts.prompts import _build_prompt , _build_context

class StudyBuddyPipeline:

    def __init__(
        self,
        vector_db: ChromaVectorDB,
        retriever: Retriever,
        llm: GroqLLM,
        memory:StudyBuddyMemory
    ):

        self.vector_db = vector_db
        self.retriever = retriever
        self.llm = llm
        self.chunker = DocumentChunker()
        self.memory = memory 

    # -------------------------
    # INGESTION
    # -------------------------

    def ingest_pdf(self, file_path: str):

        loader = DocumentLoader(file_path)

        documents = loader.load_pdf()

        chunks = self.chunker.make_chunks(documents)

        self.vector_db.add_documents(chunks)

        return {
            "pages": len(documents),
            "chunks": len(chunks)
        }
    
    def ingest_text(self, documents: str):

        loader = DocumentLoader() 
        docs = loader.load_text(documents)
        chunks = self.chunker.make_chunks(docs)
        self.vector_db.add_documents(chunks)

        return {
            "pages": len(documents),
            "chunks": len(chunks)
        }


    # -------------------------
    # RETRIEVAL
    # -------------------------

    def search_notes(self, query: str, k: int = 5):

        return self.retriever.retrieve(
            query=query,
            k=k
        )

    def get_sources(self, query: str, k: int = 5):

        documents = self.search_notes(query, k)

        sources = []

        for doc in documents:

            sources.append({
                "source": doc.metadata.get(
                    "source",
                    "Unknown source"
                ),

                "page": doc.metadata.get(
                    "page",
                    "Unknown page"
                )
            })

        return sources

    # -------------------------
    # QUESTION ANSWERING
    # -------------------------

    def ask(self,question: str,session_id: str = "default_session"):

        documents = self.search_notes(
            query=question,
            k=5
        )

        context = _build_context(documents)

        prompt = _build_prompt(
            question=question,
            context=context
        )

        answer = self.llm.invoke(prompt)

        self.memory.add_message(
            session_id=session_id,
            role="user",
            content=question
        )

        # 7. Save assistant response
        self.memory.add_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )


        return {
            "answer": answer,
            "sources": documents
        }
    