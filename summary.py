"""
Document Summarizer
"""

import json
from llm import load_llm

PROMPT = """
You are an AI Research Assistant.

Analyze the document below.

{text}

Return ONLY valid JSON.

Use this format exactly:

{{
    "title": "",
    "topics": [
        "",
        "",
        "",
        "",
        ""
    ],
    "summary": "",
    "questions": [
        "",
        "",
        "",
        "",
        ""
    ]
}}

Do not write markdown.
Do not explain anything.
Only return JSON.
"""



def generate_summary(text):

    llm = load_llm()

    response = llm.invoke(
        PROMPT.format(text=text[:5000])
    )

    try:
        data = json.loads(response.content)

    except json.JSONDecodeError:

        data = {
            "title": "Unknown",
            "topics": [],
            "summary": response.content,
            "questions": []
        }

    return data