import json

from sqlalchemy.orm import Session

from db import engine
from ingest import ingest_text
from search import search

K = 4


def contains(text, phrase):
    return " ".join(phrase.lower().split()) in " ".join(text.lower().split())


def run():
    with open("evals/questions.json", encoding="utf-8") as f:
        questions = json.load(f)
    with open("sample_docs/policy.md", encoding="utf-8") as f:
        text = f.read()

    rows = []
    with Session(engine) as session:
        ingest_text(session, "policy.md", text, size=200, overlap=30)
        for q in questions:
            hits = search(session, q["question"], k=K)
            found = q["answerable"] and any(contains(h["text"], q["gold_phrase"]) for h in hits)
            rows.append({**q, "top_score": hits[0]["score"], "found": found})
        session.rollback()
    report(rows)


def report(rows):
    answerable = [r for r in rows if r["answerable"]]
    unanswerable = [r for r in rows if not r["answerable"]]
    recall = sum(r["found"] for r in answerable) / len(answerable)
    print(f"retrieval recall@{K}: {recall:.0%} of {len(answerable)} answerable questions")
    print()
    print("threshold  wrongly answered  wrongly refused")
    for t in [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]:
        wrong_answer = sum(r["top_score"] >= t for r in unanswerable)
        wrong_refuse = sum(r["top_score"] < t for r in answerable)
        print(f"  {t:.2f}      {wrong_answer}/{len(unanswerable)}               {wrong_refuse}/{len(answerable)}")
    print()
    for r in sorted(rows, key=lambda r: r["top_score"]):
        tag = "ANSWERABLE  " if r["answerable"] else "unanswerable"
        print(f"{r['top_score']:.3f}  {tag}  {r['question']}")


if __name__ == "__main__":
    run()