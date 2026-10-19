from sqlalchemy import select

from embeddings import embed_query
from models import Chunk, Document


def search(session, question, k=4):
    query_vector = embed_query(question)
    distance = Chunk.embedding.cosine_distance(query_vector)
    rows = session.execute(
        select(Chunk, Document.filename, distance.label("distance"))
        .join(Document, Chunk.document_id == Document.id)
        .order_by(distance)
        .limit(k)
    ).all()
    return [
        {"chunk_id": chunk.id, "filename": filename, "text": chunk.text, "score": 1 - dist}
        for chunk, filename, dist in rows
    ]

MIN_SCORE = 0.5


def retrieve(session, question, k=4, min_score=MIN_SCORE):
    hits = search(session, question, k)
    answerable = bool(hits) and hits[0]["score"] >= min_score
    return {"answerable": answerable, "min_score": min_score, "hits": hits}    