from ingestion.document_loader import DocumentLoader
from ingestion.chunker import TextChunker
from ingestion.embed_worker import EmbedWorker
from core.vector_store import VectorStore


def main():

    loader = DocumentLoader()
    chunker = TextChunker()
    embedder = EmbedWorker()
    store = VectorStore()

    batch_texts = []
    batch_chunks = []

    for document in loader.load_documents():

        for chunk in chunker.chunk_document(document):

            batch_texts.append(chunk["text"])
            batch_chunks.append(chunk)

            if len(batch_texts) >= 100:

                embeddings = embedder.embed_batch(batch_texts)
                store.add_embeddings(embeddings, batch_chunks)

                batch_texts = []
                batch_chunks = []

    if batch_texts:
        embeddings = embedder.embed_batch(batch_texts)
        store.add_embeddings(embeddings, batch_chunks)

    print("Indexing complete.")


if __name__ == "__main__":
    main()