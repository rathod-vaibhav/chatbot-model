from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PERSIST_DIR = str(BASE_DIR / "vector_db")

_vectorstore = None


def _embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ---------- BUILD (RUN MANUALLY) ----------

def get_vectorstore():
    global _vectorstore

    if _vectorstore is None:
        print("⚡ Loading vector DB into memory...")

        _vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=_embeddings()
        )

    return _vectorstore