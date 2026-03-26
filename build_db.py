from app.web_crawler import load_site
from app.chunker import split_docs
from app.vector_store import build_vectorstore

print("🌐 Loading site...")
docs = load_site()

print("✂️ Splitting...")
chunks = split_docs(docs)

print("📦 Creating vector DB...")
build_vectorstore(chunks)

print("✅ DONE")