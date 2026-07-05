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

    st.markdown("""
# 🤖 DocuMind AI

<span style="color:#9CA3AF;">
Intelligent Research Assistant
</span>
""", unsafe_allow_html=True)

    st.markdown("---")

# --------------------------------
# Status
# --------------------------------

    if st.session_state.ready:

        st.success(
            f"🟢 Ready • {st.session_state.document_count} PDF(s) Loaded"
        )

    else:

        st.info(
            "📄 No documents loaded"
        )

    st.markdown("---")

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

    st.divider()

# ------------------------------------
# Analytics Dashboard
# ------------------------------------

    st.markdown("### 📊 Analytics")

    st.markdown(f"""
    <div style="
    background:#1C2128;
    padding:18px;
    border-radius:15px;
    border:1px solid #30363D;
    line-height:2;
    ">

    <b>📄 Documents</b>
    <span style="float:right;">{st.session_state.document_count}</span>
    <br>

    <b>🧩 Chunks</b>
    <span style="float:right;">{st.session_state.chunk_count}</span>
    <br>

    <b>💬 Questions</b>
    <span style="float:right;">{st.session_state.question_count}</span>
    <br>

    <b>⚡ Response</b>
    <span style="float:right;">{st.session_state.response_time:.2f} s</span>
    <br>

    <hr style="border:0.5px solid #30363D;">

    <b>🤖 Model</b><br>
    <span style="color:#58A6FF;">
    {st.session_state.model_name}
    </span>

    </div>
    """, unsafe_allow_html=True)

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

st.markdown("""
<div style="
    padding:30px;
    border-radius:18px;
    background:linear-gradient(135deg,#1E293B,#111827);
    border:1px solid #30363D;
    margin-bottom:25px;
">

<h1 style="margin:0;">
🤖 DocuMind AI
</h1>

<h3 style="color:#9CA3AF;margin-top:10px;">
AI-Powered Research Assistant
</h3>

<p style="font-size:18px;color:#D1D5DB;">
Search • Summarize • Analyze • Chat with your PDF documents using
<b>Llama 3.2</b>, <b>LangChain</b>, and <b>ChromaDB</b>.
</p>

</div>
""", unsafe_allow_html=True)



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

# ------------------------------------
# Chat Input
# ------------------------------------

    typed_question = st.chat_input(
        "Ask anything about your documents..."
    )

    question = typed_question

    if question is None and st.session_state.selected_question:

        question = st.session_state.selected_question
        st.session_state.selected_question = None

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
            start_time = time.time()

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

            st.session_state.response_time = time.time() - start_time
            st.session_state.question_count += 1

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
        # ------------------------------------
        # AI Research Summary
        # ------------------------------------

    if st.session_state.ready and st.session_state.summary:

        with st.expander("📄 AI Research Summary", expanded=True):

            st.markdown(
                f"## 📌 {st.session_state.summary['title']}"
            )

            st.markdown("### 🧩 Key Topics")

            for topic in st.session_state.summary["topics"]:

                st.markdown(f"- {topic}")

            st.markdown("### 📝 Summary")

            st.write(st.session_state.summary["summary"])

        st.divider()


# ------------------------------------
# Suggested Questions
# ------------------------------------

if st.session_state.suggested_questions:

    st.subheader("💡 Suggested Questions")

    for i, question in enumerate(st.session_state.suggested_questions):

        if st.button(
            f"💬 {question}",
            key=f"suggestion_{i}",
            use_container_width=True,
        ):
            st.session_state.selected_question = question
            #st.rerun()

    st.divider()
    #st.rerun()

st.divider()

st.caption(
    "🚀 Powered by Ollama • LangChain • ChromaDB • HuggingFace"
)