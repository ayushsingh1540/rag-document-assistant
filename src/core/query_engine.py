import ollama
import numpy as np
from sentence_transformers import SentenceTransformer


class QueryEngine:

    def __init__(self, vector_store, memory):
        self.store = vector_store
        self.memory = memory
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def ask(self, user, question):

        # Create embedding
        query_vec = self.model.encode([question]).astype("float32")

        # Search FAISS
        context_chunks = self.store.search(query_vec, top_k=3)

        context = "\n".join(context_chunks)

        history = "\n".join(self.memory.get_history(user, k=2))

        prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}

Answer briefly.
"""

        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response["message"]["content"]

        # Save conversation
        self.memory.save(user, f"User: {question}")
        self.memory.save(user, f"Assistant: {answer}")

        return answer