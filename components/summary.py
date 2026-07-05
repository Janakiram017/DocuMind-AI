import streamlit as st


def render_summary():

    if (
        st.session_state.ready
        and st.session_state.summary
    ):

        with st.expander(
            "📄 AI Research Summary",
            expanded=True,
        ):

            st.markdown(
                f"## 📌 {st.session_state.summary['title']}"
            )

            st.markdown("### 🧩 Key Topics")

            for topic in st.session_state.summary["topics"]:

                st.markdown(f"- {topic}")

            st.markdown("### 📝 Summary")

            st.write(
                st.session_state.summary["summary"]
            )

        st.divider()