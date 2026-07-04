"""
Application Configuration
"""

from pathlib import Path

# ----------------------------------------------------
# Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).parent

UPLOAD_FOLDER = BASE_DIR / "uploads"

VECTOR_DB = BASE_DIR / "chroma_db"

LOG_FOLDER = BASE_DIR / "logs"

# ----------------------------------------------------
# LLM
# ----------------------------------------------------

OLLAMA_MODEL = "llama3.2"

TEMPERATURE = 0

# ----------------------------------------------------
# Embeddings
# ----------------------------------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ----------------------------------------------------
# RAG
# ----------------------------------------------------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K_RESULTS = 4

# ----------------------------------------------------
# UI
# ----------------------------------------------------

APP_NAME = "DocuMind AI"

PAGE_TITLE = "📚 DocuMind AI"

PAGE_ICON = "🤖"

WELCOME_MESSAGE = """
Upload one or more PDF files and start chatting with them.

Powered by:

• Ollama
• Llama 3.2
• LangChain
• ChromaDB
• HuggingFace Embeddings
"""