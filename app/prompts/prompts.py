def _build_context(documents):

    return "\n\n".join(
        document.page_content
        for document in documents
    )

def _build_prompt(
        question: str,
        context: str,
        history: str = ""
    ):
        history_section = ""
        if history:
            history_section = f"\nConversation History:\n{history}\n--------------------\n"

        return f"""
You are a helpful study assistant.

Answer the user's question using the provided context.
{history_section}
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
