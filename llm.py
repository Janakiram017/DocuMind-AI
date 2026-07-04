"""
LLM Loader
"""

from langchain_ollama import ChatOllama

from config import OLLAMA_MODEL
from config import TEMPERATURE


def load_llm():

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=TEMPERATURE,
    )

    return llm