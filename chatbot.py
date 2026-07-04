from langchain_core.prompts import ChatPromptTemplate

from llm import load_llm
from config import TOP_K_RESULTS

SYSTEM_PROMPT = """
You are DocuMind AI.

Answer ONLY using the uploaded documents.

Conversation History:
{history}

Document Context:
{context}

Current Question:
{question}

Instructions:
- Use the conversation history.
- If the answer is not in the documents, say:
  "I couldn't find this information in the uploaded documents."
- Keep answers clear and concise.
"""

def retrieve_context(vectorstore, question):

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": TOP_K_RESULTS}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context, docs


def stream_answer(context, question, history=""):

    prompt = ChatPromptTemplate.from_template(
        SYSTEM_PROMPT
    )

    chain = prompt | load_llm()

    return chain.stream(
        {
            "history": history,
            "context": context,
            "question": question,
        }
    )