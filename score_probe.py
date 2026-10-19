from sqlalchemy.orm import Session

from db import engine
from ingest import ingest_text
from search import search

ANSWERABLE = [
    "What's the limit for dinner on a work trip?",
    "Do I need approval to buy something expensive?",
    "How soon must I report a stolen work laptop?",
]

UNANSWERABLE = [
    "How many vacation days do I get?",
    "What is the process for requesting a salary raise?",
    "Which airline should I book for business travel?",
]


def run():
    with open("sample_docs/policy.md", encoding="utf-8") as f:
        text = f.read()
    with Session(engine) as session:
        ingest_text(session, "policy.md", text, size=200, overlap=30)
        for label, questions in (("ANSWERABLE", ANSWERABLE), ("UNANSWERABLE", UNANSWERABLE)):
            print(label)
            for question in questions:
                top = search(session, question, k=1)[0]
                print(f"  {top['score']:.3f}  {question}")
        session.rollback()


if __name__ == "__main__":
    run()