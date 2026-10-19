from sqlalchemy.orm import Session

from answer import answer_question
from db import engine
from ingest import ingest_text

QUESTIONS = [
    "What's the limit for dinner on a work trip?",
    "How soon must I report a stolen work laptop?",
    "How many vacation days do I get?",
    "How do I submit an expense claim in the system?",
]

with open("sample_docs/policy.md", encoding="utf-8") as f:
    text = f.read()

with Session(engine) as session:
    ingest_text(session, "policy.md", text, size=200, overlap=30)
    for question in QUESTIONS:
        result = answer_question(session, question)
        print("Q:", question)
        print("  answered:", result["answered"], "| reason:", result["reason"])
        print("  answer:", result["answer"])
        for c in result["citations"]:
            print("  cited:", c["filename"], round(c["score"], 3), "-", c["excerpt"][:60])
        print()
    session.rollback()