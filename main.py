from app.pipeline.pipeline import StudyBuddyPipeline
from app.embedding.embedder import EmbeddingModel
from app.vector_db.chromadb import ChromaVectorDB
from app.retriever.retriever import Retriever
from app.rag.llm import GroqLLM
from app.pipeline.pipeline import StudyBuddyPipeline
from app.memory.memory import StudyBuddyMemory

embedding = EmbeddingModel()

vector_db = ChromaVectorDB(
    embedding_function=embedding.get_embedding_model()
)

retriever = Retriever(
    vector_db=vector_db
)

llm = GroqLLM()

memory = StudyBuddyMemory()
# -------------------------
# CENTRAL PIPELINE
# -------------------------

study_pipeline = StudyBuddyPipeline(
    vector_db=vector_db,
    retriever=retriever,
    llm=llm,
    memory= memory
)

print(study_pipeline.ask("What is management"))