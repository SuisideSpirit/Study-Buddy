from pathlib import Path

from langchain_chroma import Chroma
from config import COLLECTION_NAME , DATABASE_PATH
from app.embedding.embedder import EmbeddingModel


class ChromaVectorDB:

    def __init__(
        self,embedding_model ,
        collection_name: str = COLLECTION_NAME,
        persist_directory: str = DATABASE_PATH
    ):

        self.persist_directory = Path(persist_directory)

        self.embedding_function = embedding_model

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_function,
            persist_directory=str(self.persist_directory),
        )

    def add_documents(self, documents):
        """
        Add LangChain documents to ChromaDB
        """
        self.vector_store.add_documents(documents)

    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):
        """
        Retrieve top-k most similar chunks.
        """
        return self.vector_store.similarity_search(
            query=query,
            k=k
        )

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5
    ):
        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k
        )

    def as_retriever(self, k: int = 5):
        return self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )

    def count(self):
        return self.vector_store._collection.count()

    def delete_collection(self):
        self.vector_store.delete_collection()