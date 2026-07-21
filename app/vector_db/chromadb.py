from pathlib import Path

from langchain_chroma import Chroma
from config import COLLECTION_NAME, DATABASE_PATH


class ChromaVectorDB:

    def __init__(
        self,
        embedding_function,
        collection_name: str = COLLECTION_NAME,
        persist_directory: str = DATABASE_PATH
    ):

        self.persist_directory = Path(persist_directory)

        # Make sure the directory exists and is writable
        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.embedding_function = embedding_function

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_function,
            persist_directory=str(self.persist_directory),
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(
            query=query,
            k=k
        )

    def similarity_search_with_score(self, query: str, k: int = 5):
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

    def get_chunks_by_source(self, source_name: str):
        res = self.vector_store.get()
        documents = res.get("documents", [])
        metadatas = res.get("metadatas", [])

        matching_docs = []
        for doc, meta in zip(documents, metadatas):
            meta_source = meta.get("source", "")
            if source_name in meta_source or meta_source.endswith(source_name):
                matching_docs.append(doc)
        return matching_docs