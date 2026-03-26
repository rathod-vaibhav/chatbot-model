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
def build_vectorstore(documents):
    db = Chroma.from_documents(
        documents,
        embedding=_embeddings(),
        persist_directory=PERSIST_DIR
    )

    print("✅ Vector DB built with", len(documents), "documents")

    return db


# ---------- LOAD (USED BY CHATBOT) ----------
def get_vectorstore():
    global _vectorstore

    if _vectorstore is None:
        print("⚡ Loading vector DB into memory...")

        _vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=_embeddings()
        )

        # sanity check
        if _vectorstore._collection.count() == 0:
            raise Exception(
                "Vector DB is empty! Run build_vectorstore() first."
            )

    return _vectorstore
