import streamlit as st


def render_sidebar():

    st.markdown("""
# 🤖 DocuMind AI

<span style="color:#9CA3AF;">
Intelligent Research Assistant
</span>
""", unsafe_allow_html=True)

    st.markdown("---")

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

    return uploaded_files, process, clear