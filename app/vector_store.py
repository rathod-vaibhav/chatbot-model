from pathlib import Path
from langchain_chroma import Chroma
from .embeddings import get_embeddings

BASE_DIR = Path(__file__).resolve().parent.parent
PERSIST_DIR = str(BASE_DIR / "vector_db")

_vectorstore = None


# ---------- BUILD (RUN MANUALLY) ----------

def build_vectorstore(chunks):
    print(f"📦 Creating vector DB with {len(chunks)} chunks...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=PERSIST_DIR
    )
    print("✅ Vector DB built and persisted.")
    return vectorstore


def get_vectorstore():
    global _vectorstore

    if _vectorstore is None:
        print("⚡ Loading vector DB into memory...")

        _vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=get_embeddings()
        )

    return _vectorstore