from fastmcp import FastMCP

from app.embedding.embedder import EmbeddingModel
from app.vector_db.chromadb import ChromaVectorDB
from app.retriever.retriever import Retriever
from app.rag.llm import GroqLLM
from app.rag.pipeline import RAGPipeline


# Create FastMCP server
mcp = FastMCP("Study Buddy")


# Initialize components once
embedding = EmbeddingModel()

vector_db = ChromaVectorDB(
    embedding_function=embedding.get_embedding_model()
)

retriever = Retriever(
    vector_db=vector_db,
    k=3
)

llm = GroqLLM()

rag_pipeline = RAGPipeline(
    retriever=retriever,
    llm=llm
)


@mcp.tool()
def ask_study_question(question: str) -> str:
    """
    Answer a study question using the uploaded study material.
    """

    result = rag_pipeline.ask(question)

    return result["answer"]


if __name__ == "__main__":
    mcp.run()