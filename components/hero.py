import streamlit as st


def render_hero():

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