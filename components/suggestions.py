import streamlit as st


def render_suggestions():

    if not st.session_state.suggested_questions:
        return

    st.subheader("💡 Suggested Questions")

    for i, question in enumerate(st.session_state.suggested_questions):

        if st.button(
            f"💬 {question}",
            key=f"suggestion_{i}",
            use_container_width=True,
        ):
            st.session_state.selected_question = question

    st.divider()