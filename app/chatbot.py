# from langchain_ollama import ChatOllama
# from .vector_store import get_vectorstore


# def ask_ai(question: str) -> str:
#     vectordb = get_vectorstore()

#     # search similar docs
#     docs = vectordb.similarity_search(question, k=3)

#     # combine context
#     context = "\n\n".join([doc.page_content for doc in docs])

#     # LLM
#     llm = ChatOllama(
#         model="phi3:mini",
#         temperature=0
#     )

#     # prompt
#     prompt = f"""
# You are a professional assistant answering questions about Vaibhav's portfolio.

# Use the context below to answer clearly.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """

#     response = llm.invoke(prompt)

#     return response.content

import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from .vector_store import get_vectorstore

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODELS_URL = os.getenv("GROQ_MODELS_URL")

def get_best_model() -> str:
    """Fetch all models from Groq and return the one with highest max_completion_tokens."""
    url = GROQ_MODELS_URL
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        models = data.get("data", [])
        if not models:
            return "mixtral-8x7b-32768"  # Fallback
            
        # Sort by max_completion_tokens descending
        sorted_models = sorted(
            models, 
            key=lambda x: x.get("max_completion_tokens", 0), 
            reverse=True
        )
        
        # Filter for models that are likely to be chat models (heuristic: excluding whisper/guard if possible)
        # But based on the provided list, llama-3.1-8b-instant has 131k, and others are also chat models.
        # Let's just pick the top one as requested.
        return sorted_models[0]["id"]
    except Exception as e:
        print(f"Error fetching models: {e}")
        return "mixtral-8x7b-32768"  # Fallback


def ask_ai(question: str) -> str:
    vectordb = get_vectorstore()

    docs = vectordb.similarity_search(question, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    selected_model = get_best_model()
    print(f"Using model: {selected_model}")

    llm = ChatGroq(
        model=selected_model,
        api_key=GROQ_API_KEY
    )

    prompt = f"""
Answer based on this portfolio:

{context}

Question: {question}
"""

    response = llm.invoke(prompt)

    return response.content