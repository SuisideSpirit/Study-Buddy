from app.vector_db.chromadb import ChromaVectorDB


class Retriever:

    def __init__(self,vector_db: ChromaVectorDB):
        self.vector_db = vector_db

    def retrieve( self, query: str ,k :int ):
        """
        Retrieve the top-k most relevant documents.
        """
        return self.vector_db.similarity_search(
            query=query,
            k=k
        )

    def retrieve_with_score(self, query: str ,k : int ):
        """
        Retrieve documents along with their similarity scores.
        """
        return self.vector_db.similarity_search_with_score(
            query=query,
            k= k
        )