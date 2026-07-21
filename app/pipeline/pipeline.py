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

    def ask(self, question: str, session_id: str = "default_session"):
        # Retrieve recent history (last 5 messages) from SQLite
        history_messages = self.memory.get_history(session_id, limit=5)
        formatted_history = "\n".join(
            f"{role.capitalize()}: {content}"
            for role, content in history_messages
        )

        documents = self.search_notes(
            query=question,
            k=5
        )

        context = _build_context(documents)

        prompt = _build_prompt(
            question=question,
            context=context,
            history=formatted_history
        )

        answer = self.llm.invoke(prompt)

        # Save messages to chat history
        self.memory.add_message(
            session_id=session_id,
            role="user",
            content=question
        )

        self.memory.add_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )

        # Log study progress
        self.memory.add_progress(
            session_id=session_id,
            action_type="query",
            target_name=question[:40] + "...",
            details="Asked study question."
        )

        return {
            "answer": answer,
            "sources": documents
        }

    def summarize_document(self, document_name: str, session_id: str = "default_session") -> str:
        chunks = self.vector_db.get_chunks_by_source(document_name)
        if not chunks:
            return f"No document chunks found matching '{document_name}' in the vector database."

        combined_text = "\n\n".join(chunks[:30])

        prompt = f"""
You are a helpful study assistant.

Please provide a clear, comprehensive, and structured summary of the following document.
Use bullet points and clear headings where appropriate.

Document Name: {document_name}
--------------------
{combined_text}
--------------------

Summary:
"""
        summary = self.llm.invoke(prompt)

        # Log progress
        self.memory.add_progress(
            session_id=session_id,
            action_type="summarize",
            target_name=document_name,
            details=f"Generated summary using {len(chunks)} document chunks."
        )

        return summary

    def get_study_progress(self, session_id: str = "default_session") -> str:
        history = self.memory.get_history(session_id, limit=100)
        num_questions = len([role for role, _ in history if role == "user"])

        progress_entries = self.memory.get_progress(session_id)

        if not progress_entries and num_questions == 0:
            return f"No study progress logged yet for session '{session_id}'."

        summaries_done = [target for action, target, _, _ in progress_entries if action == "summarize"]

        report = []
        report.append(f"### Study Progress Report (Session: `{session_id}`)")
        report.append(f"- **Total Questions Asked**: {num_questions}")
        report.append(f"- **Documents Summarized**: {len(summaries_done)}")
        for doc in set(summaries_done):
            report.append(f"  - {doc}")

        report.append("\n**Recent Activity Log**:")
        for action, target, details, timestamp in progress_entries[:5]:
            report.append(f"- `[{timestamp}]` {action.upper()}: {target} ({details})")

        return "\n".join(report)
    