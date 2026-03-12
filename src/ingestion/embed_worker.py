from sentence_transformers import SentenceTransformer
import numpy as np

class EmbedWorker:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_batch(self, texts):
        return self.model.encode(
            texts,
            batch_size=64,
            convert_to_numpy=True
        )