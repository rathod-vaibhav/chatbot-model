from fastapi import FastAPI
from pydantic import BaseModel
from app.chatbot import ask_ai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str


@app.post("/ask")
def ask_question(data: Query):
    answer = ask_ai(data.query)
    return {"answer": answer}