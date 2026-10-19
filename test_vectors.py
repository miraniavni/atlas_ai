from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine
from models import EMBEDDING_DIM, Base, Chunk, Document


def vec(*head):
    return list(head) + [0.0] * (EMBEDDING_DIM - len(head))


def test_nearest_chunk_is_found():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        doc = Document(filename="test.md", sha256="x" * 64)
        session.add(doc)
        session.flush()
        session.add_all([
            Chunk(document_id=doc.id, chunk_index=0, text="about cats",
                  embedding=vec(1.0, 0.0)),
            Chunk(document_id=doc.id, chunk_index=1, text="about cars",
                  embedding=vec(0.0, 1.0)),
        ])
        session.flush()

        query = vec(0.9, 0.1)
        nearest = session.scalars(
            select(Chunk).order_by(Chunk.embedding.cosine_distance(query)).limit(1)
        ).first()

        assert nearest.text == "about cats"
        session.rollback()