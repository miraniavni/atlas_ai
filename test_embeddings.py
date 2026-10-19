import numpy as np

from embeddings import embed_documents, embed_query
from models import EMBEDDING_DIM


def test_embedding_has_expected_size():
    vectors = embed_documents(["hello world"])
    assert len(vectors) == 1
    assert len(vectors[0]) == EMBEDDING_DIM


def test_relevant_passage_scores_higher():
    passages = [
        "Employees must submit expense receipts within 30 days of purchase.",
        "The office cafeteria serves lunch from noon to two.",
    ]
    doc_vectors = np.array(embed_documents(passages))
    query = np.array(embed_query("How long do I have to submit receipts?"))
    scores = doc_vectors @ query
    print("scores:", scores)
    assert scores[0] > scores[1]