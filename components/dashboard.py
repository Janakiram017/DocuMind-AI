import streamlit as st


def render_dashboard():

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