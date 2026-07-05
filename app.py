"""
DocuMind AI
Main Application
"""

import os
import time
import streamlit as st

from config import *
from rag import process_pdf
from vectorstore import build_vectorstore
from chatbot import retrieve_context, stream_answer
from utils import clear_database, clear_uploads, format_sources
from summary import generate_summary
from components.sidebar import render_sidebar
from components.hero import render_hero
from components.dashboard import render_dashboard
from components.summary import render_summary
from components.suggestions import render_suggestions
from components.chat import (
    render_chat_history,
    render_chat_input,
    render_assistant_response,
)
# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)
# ------------------------------------
# Load Custom CSS
# ------------------------------------

def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

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

if "suggested_questions" not in st.session_state:
    st.session_state.suggested_questions = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None

if "document_count" not in st.session_state:
    st.session_state.document_count = 0

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "response_time" not in st.session_state:
    st.session_state.response_time = 0.0

if "model_name" not in st.session_state:
    st.session_state.model_name = OLLAMA_MODEL
# ------------------------------------
# Sidebar
# ------------------------------------

with st.sidebar:

    uploaded_files, process, clear = render_sidebar()



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
            st.session_state.document_count = len(uploaded_files)
            st.session_state.chunk_count = len(documents)
            
            st.session_state.ready = True

        preview = "\n".join(
            doc.page_content
            for doc in documents[:5]
        )

        with st.spinner("Generating AI Summary..."):

            data = generate_summary(preview)

            st.session_state.summary = data
            st.session_state.suggested_questions = data["questions"]

        st.success("✅ Documents processed successfully!")

        # st.rerun()
# ------------------------------------
# Main Page
# ------------------------------------

render_hero()



if not st.session_state.ready:

    st.info(
        "👈 Upload PDF documents and click **Process Documents**."
    )

else:

    # Display previous conversation
    render_chat_history()
# ------------------------------------
# AI Research Summary
# ------------------------------------
    
    render_summary()

# ------------------------------------
# Chat Input
# ------------------------------------

    question = render_chat_input()

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

            render_assistant_response(question)


# ------------------------------------
# Suggested Questions
# ------------------------------------

render_suggestions()
    #st.rerun()

st.divider()

st.caption(
    "🚀 Powered by Ollama • LangChain • ChromaDB • HuggingFace"
)