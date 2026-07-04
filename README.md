# 🤖 DocuMind AI

> An AI-powered Research Assistant that lets you chat with your PDF documents using **Local LLMs (Llama 3.2)**, **LangChain**, and **ChromaDB**.

---

## 🚀 Features

- 📄 Upload one or multiple PDF documents
- 🧠 AI-generated document summary
- 💬 Chat with your PDFs
- 🔍 Semantic Search using ChromaDB
- 🧠 Conversation Memory
- 📑 Source References
- 🖥️ Runs completely offline using Ollama
- ⚡ Powered by Llama 3.2

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | User Interface |
| Ollama | Local LLM |
| Llama 3.2 | Language Model |
| LangChain | RAG Pipeline |
| ChromaDB | Vector Database |
| HuggingFace | Embeddings |
| PyPDF | PDF Processing |

---

## 📂 Project Structure

```text
DocuMind-AI/
│
├── app.py
├── chatbot.py
├── config.py
├── llm.py
├── rag.py
├── summary.py
├── utils.py
├── vectorstore.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── chroma_db/
├── uploads/
└── assets/
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Janakiram017/DocuMind-AI.git
```

Move into the project

```bash
cd DocuMind-AI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Ollama

https://ollama.com

Download Llama 3.2

```bash
ollama pull llama3.2
```

Run the application

```bash
streamlit run app.py
```

---

## 📸 Application Preview

> Screenshots will be added soon.

---

## 🧠 How it Works

```text
PDF
      │
      ▼
Document Loader
      │
      ▼
Text Splitter
      │
      ▼
Embeddings
      │
      ▼
ChromaDB
      │
      ▼
Retriever
      │
      ▼
Llama 3.2 (Ollama)
      │
      ▼
Answer
```

---

## 📈 Future Improvements

- ChatGPT-style streaming responses
- PDF Preview
- Export Chat
- Authentication
- Docker Support
- Cloud Deployment
- Hybrid Search
- Analytics Dashboard

---

## 👨‍💻 Author

**Janakiram R S**

GitHub:

https://github.com/Janakiram017

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.