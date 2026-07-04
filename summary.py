"""
Document Summarizer
"""

from llm import load_llm

PROMPT = """
You are an AI Research Assistant.

Below is the beginning of a document.

{text}

Generate:

1. Document Title

2. Five Key Topics

3. A short summary (150 words max)

4. Five questions the user can ask.

Return in markdown.
"""

def generate_summary(text):

    llm = load_llm()

    response = llm.invoke(
        PROMPT.format(text=text[:5000])
    )

    return response.content