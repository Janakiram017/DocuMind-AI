"""
Vector Database
"""

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma

from config import *


def load_embeddings():

    return HuggingFaceEmbeddings(

        model_name=EMBEDDING_MODEL

    )


def build_vectorstore(documents):

    embeddings = load_embeddings()

    db = Chroma.from_documents(

        documents=documents,

        embedding=embeddings,

        persist_directory=str(VECTOR_DB)

    )

    return db