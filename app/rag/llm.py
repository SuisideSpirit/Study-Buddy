from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqLLM:

    def __init__(
        self,
        model_name: str = "llama-3.3-70b-versatile",
        temperature: float = 0.2
    ):

        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            groq_api_key=GROQ_API_KEY
        )

    def invoke(self, prompt: str) -> str:

        response = self.llm.invoke(prompt)

        return response.content