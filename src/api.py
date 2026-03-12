from fastapi import FastAPI
from pydantic import BaseModel

from src.core.query_engine import QueryEngine
from src.core.vector_store import VectorStore
from src.core.memory import ChatMemory


app = FastAPI()

# Initialize dependencies
vector_store = VectorStore()
memory = ChatMemory()
engine = QueryEngine(vector_store, memory)


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QueryRequest):

    answer = engine.ask("default_user", request.question)

    return {"answer": answer}