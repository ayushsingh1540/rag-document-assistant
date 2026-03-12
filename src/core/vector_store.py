import faiss
import sqlite3
import numpy as np
import os


class VectorStore:

    def __init__(self, dim=384):

        os.makedirs("vector_db", exist_ok=True)

        self.index_path = "vector_db/faiss.index"
        self.db_path = "vector_db/metadata.sqlite"
        self.dim = dim

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._create_table()

        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            # temporary index, will be replaced when we know dataset size
            self.index = None

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT,
                chunk_id INTEGER,
                text TEXT
            )
        """)
        self.conn.commit()

    def _create_index(self, embeddings):

        n_vectors = embeddings.shape[0]

        # dynamic cluster size
        nlist = min(50, max(1, n_vectors // 10))

        quantizer = faiss.IndexFlatL2(self.dim)
        index = faiss.IndexIVFFlat(quantizer, self.dim, nlist)
        index.nprobe = 5

        index.train(embeddings)

        return index

    def add_embeddings(self, embeddings, chunks):

        embeddings = np.array(embeddings).astype("float32")

        # Create index if it doesn't exist
        if self.index is None:
            self.index = self._create_index(embeddings)

        # Train if not trained
        if not self.index.is_trained:
            self.index.train(embeddings)

        self.index.add(embeddings)

        for chunk in chunks:
            self.conn.execute(
                "INSERT INTO chunks (doc_id, chunk_id, text) VALUES (?, ?, ?)",
                (chunk["doc_id"], chunk["chunk_id"], chunk["text"])
            )

        self.conn.commit()

        faiss.write_index(self.index, self.index_path)

    def search(self, query_vector, top_k=5):

        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = np.array(query_vector).astype("float32")

        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            row = self.conn.execute(
                "SELECT text FROM chunks LIMIT 1 OFFSET ?",
                (int(idx),)
            ).fetchone()

            if row:
                results.append(row[0])

        return results