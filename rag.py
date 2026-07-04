"""
PDF Processing
"""

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import *


def load_pdf(path):

    loader = PyPDFLoader(path)

    return loader.load()


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP

    )

    return splitter.split_documents(documents)


def process_pdf(path):

    docs = load_pdf(path)

    docs = split_documents(docs)

    return docs