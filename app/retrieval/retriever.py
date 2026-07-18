from app.vector_db.chromadb import ChromaVectorDB


class Retriever:

    def __init__(
        self,
        vector_db: ChromaVectorDB,
        k: int = 5
    ):
        self.vector_db = vector_db
        self.k = k

    def retrieve(self, query: str):
        """
        Retrieve the top-k most relevant documents.
        """
        return self.vector_db.similarity_search(
            query=query,
            k=self.k
        )

    def retrieve_with_score(self, query: str):
        """
        Retrieve documents along with their similarity scores.
        """
        return self.vector_db.similarity_search_with_score(
            query=query,
            k=self.k
        )