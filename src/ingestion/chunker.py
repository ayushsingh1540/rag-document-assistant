class TextChunker:

    def __init__(self, chunk_size=1000, overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document):

        text = document["content"]
        doc_id = document["doc_id"]

        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + self.chunk_size
            yield {
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "text": text[start:end]
            }

            start += self.chunk_size - self.overlap
            chunk_id += 1