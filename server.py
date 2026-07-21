from fastmcp import FastMCP

from app.embedding.embedder import EmbeddingModel
from app.vector_db.chromadb import ChromaVectorDB
from app.retriever.retriever import Retriever
from app.rag.llm import GroqLLM
from app.pipeline.pipeline import StudyBuddyPipeline

mcp = FastMCP("Study Buddy")

# -------------------------
# INITIALIZE COMPONENTS
# -------------------------
embedding = EmbeddingModel()

vector_db = ChromaVectorDB(embedding_function=embedding.get_embedding_model())

retriever = Retriever(vector_db=vector_db)

llm = GroqLLM()

# -------------------------
# CENTRAL PIPELINE
# -------------------------

study_pipeline = StudyBuddyPipeline(
    vector_db=vector_db,
    retriever=retriever,
    llm=llm
)


# -------------------------
# MCP TOOLS
# -------------------------

@mcp.tool()
def ask_study_question(question: str) -> str:
    """
    Answer a study question using the uploaded study material.
    """
    result = study_pipeline.ask(question)

    return result["answer"]


@mcp.tool()
def search_notes(query: str,k: int = 5) -> str:
    """
    Search the uploaded study material for relevant notes.
    """
    documents = study_pipeline.search_notes(
        query=query,
        k=k
    )

    if not documents:
        return "No relevant notes found."

    results = []

    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get(
            "source",
            "Unknown source"
        )
        page = doc.metadata.get(
            "page",
            "Unknown page"
        )
        results.append(f"""
            Result {i}
            Source: {source}
            Page: {page}
            {doc.page_content}
            """)

    return "\n".join(results)


@mcp.tool()
def get_sources(query: str, k: int = 5) -> str:
    """
    Get the sources used for a query.
    """
    sources = study_pipeline.get_sources(query=query,k=k)

    if not sources:
        return "No sources found."

    return "\n".join(
        f"{i}. Source: {source['source']} | "
        f"Page: {source['page']}"
        for i, source in enumerate(sources, start=1)
    )

if __name__ == "__main__":
    mcp.run()