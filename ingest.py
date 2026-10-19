import hashlib

from sqlalchemy import select

from chunking import chunk_text
from embeddings import embed_documents
from models import Chunk, Document


def ingest_text(session, filename, text, size=500, overlap=80):
    if not text.strip():
        raise ValueError("document has no text")

    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    existing = session.scalars(select(Document).where(Document.sha256 == sha)).first()
    if existing:
        return existing, False

    pieces = chunk_text(text, size, overlap)
    vectors = embed_documents(pieces)

    doc = Document(filename=filename, sha256=sha)
    session.add(doc)
    session.flush()
    for i, (piece, vector) in enumerate(zip(pieces, vectors)):
        session.add(Chunk(document_id=doc.id, chunk_index=i, text=piece, embedding=vector))
    session.flush()
    return doc, True