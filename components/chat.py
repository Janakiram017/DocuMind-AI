import streamlit as st
import time

from chatbot import retrieve_context, stream_answer
from utils import format_sources

def render_chat_history():

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


def render_chat_input():

    typed_question = st.chat_input(
        "Ask anything about your documents..."
    )

    question = typed_question

    if (
        question is None
        and st.session_state.selected_question
    ):

        question = st.session_state.selected_question
        st.session_state.selected_question = None

    return question
def render_assistant_response(question):

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

    st.session_state.response_time = (
        time.time() - start_time
    )

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