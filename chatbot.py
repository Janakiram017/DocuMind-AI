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
- Use the conversation history to understand follow-up questions.
- If the answer is not present in the documents, say:
  "I couldn't find this information in the uploaded documents."
- Keep answers clear and concise.
"""

def ask_question(vectorstore, question, history=""):

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": TOP_K_RESULTS}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = ChatPromptTemplate.from_template(
        SYSTEM_PROMPT
    )

    chain = prompt | load_llm()

    response = chain.invoke({
        "history": history,
        "context": context,
        "question": question
    })

    return response.content, docs