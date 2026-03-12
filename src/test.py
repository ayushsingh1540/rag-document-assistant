from document_processor import DocumentProcessor
from chunker import TextChunker
from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore


# Step 1 — Read document

processor = DocumentProcessor(r"C:\VisualStudio\RAG_TOOL\venv\Docs\FS_ORA-352_DD_BulkInterface_StatusAndAccountingManagement.docx")

text = processor.process_document()


# Step 2 — Chunk

chunker = TextChunker(chunk_size=1500, overlap=200)

chunks = chunker.chunk_text(text)

print("Chunks created:", len(chunks))


# Step 3 — Embeddings

embedder = EmbeddingGenerator()

embeddings = embedder.generate_embeddings(chunks)


# Step 4 — Store

vector_store = VectorStore()

vector_store.create_index(embeddings, chunks)

vector_store.save()