from app.retrieval.retriever import Retriever
from app.rag.llm import GroqLLM


class RAGPipeline:

    def __init__(
        self,
        retriever: Retriever,
        llm: GroqLLM
    ):
        self.retriever = retriever
        self.llm = llm

    def _build_context(self, documents):

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        return context

    def _build_prompt(
        self,
        question: str,
        context: str
    ):

        return f"""
You are a helpful study assistant.

Answer the user's question using the provided context.

Rules:
1. Use the context as the primary source of information.
2. If the answer cannot be found in the context, say that you do not have enough information.
3. Do not make up facts.
4. Explain the answer clearly and simply.
5. Use examples when helpful.

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
"""

    def ask(self, question: str):

        documents = self.retriever.retrieve(question)

        context = self._build_context(documents)

        prompt = self._build_prompt(
            question=question,
            context=context
        )

        answer = self.llm.invoke(prompt)

        return {
            "answer": answer,
            "sources": documents
        }