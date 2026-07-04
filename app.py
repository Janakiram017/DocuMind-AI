"""
DocuMind AI
Main Application
"""

import os
import streamlit as st

from config import *
from rag import process_pdf
from vectorstore import build_vectorstore
from chatbot import retrieve_context, stream_answer
from utils import clear_database, clear_uploads, format_sources
from summary import generate_summary

# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)

# ------------------------------------
# Session State
# ------------------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ready" not in st.session_state:
    st.session_state.ready = False

if "summary" not in st.session_state:
    st.session_state.summary = ""

# ------------------------------------
# Sidebar
# ------------------------------------

with st.sidebar:

    st.title("🤖 DocuMind AI")

    st.caption("Intelligent Research Assistant")

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    process = st.button(
        "📚 Process Documents",
        use_container_width=True
    )

    clear = st.button(
        "🗑 Clear Chat",
        use_container_width=True
    )

# ------------------------------------
# Clear Chat
# ------------------------------------

if clear:
    st.session_state.messages = []
    st.rerun()

# ------------------------------------
# Process PDFs
# ------------------------------------

if process:

    if not uploaded_files:

        st.warning("Please upload at least one PDF.")

    else:

        clear_uploads()
        clear_database()

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        documents = []

        with st.spinner("Processing PDFs..."):

            for pdf in uploaded_files:

                path = os.path.join(
                    UPLOAD_FOLDER,
                    pdf.name
                )

                with open(path, "wb") as f:
                    f.write(pdf.read())

                docs = process_pdf(path)

                documents.extend(docs)

            st.session_state.vectorstore = build_vectorstore(
                documents
            )

        st.session_state.ready = True

        preview = "\n".join(
            doc.page_content
            for doc in documents[:5]
        )

        with st.spinner("Generating AI Summary..."):

            st.session_state.summary = generate_summary(preview)

        st.success("✅ Documents processed successfully!")
# ------------------------------------
# Main Page
# ------------------------------------

st.title("📚 DocuMind AI")

st.markdown(
    "### Chat with your documents using **Llama 3.2**"
)

st.divider()
# ------------------------------------
# AI Research Summary
# ------------------------------------

if st.session_state.ready and st.session_state.summary:

    st.subheader("📄 AI Research Summary")

    st.markdown(st.session_state.summary)

    st.divider()

if not st.session_state.ready:

    st.info(
        "👈 Upload PDF documents and click **Process Documents**."
    )

else:

    # Display previous conversation
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and "sources" in message
            ):

                with st.expander("📄 Sources"):

                    for source in message["sources"]:

                        st.write(source)

    # Chat Input
    question = st.chat_input(
        "Ask anything about your documents..."
    )

    if question:

        # User message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        # Assistant message
        with st.chat_message("assistant"):

            history = ""

            for msg in st.session_state.messages[-6:]:

                history += f"{msg['role']}: {msg['content']}\n"

            context, docs = retrieve_context(
                st.session_state.vectorstore,
                question
            )

            stream = stream_answer(
                context,
                question,
                history
            )

            response_placeholder = st.empty()

            answer = ""

            for chunk in stream:

                if hasattr(chunk, "content"):

                    answer += chunk.content

                    response_placeholder.markdown(
                        answer + "▌"
                    )

            response_placeholder.markdown(answer)

            sources = format_sources(docs)

            with st.expander("📄 Sources"):

                for source in sources:

                    st.write(source)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }
        )

st.divider()

st.caption(
    "🚀 Powered by Ollama • LangChain • ChromaDB • HuggingFace"
)