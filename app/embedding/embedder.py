from langchain_huggingface import HuggingFaceEmbeddings
import torch

class EmbeddingModel:

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5"
    ):
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True},
        )

    def get_embedding_model(self):
        return self.embedding_model