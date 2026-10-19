from sqlalchemy.orm import Session

from db import engine
from ingest import ingest_text
from search import search

POLICY = (
    "Expense policy. Employees must submit expense receipts within 30 days of purchase. "
    "Meals while travelling are reimbursed up to 40 dollars per day. "
    "Any single expense above 500 dollars needs written manager approval before purchase. "
    "Remote work policy. Employees may work remotely up to two days per week. "
    "Core hours are 11 am to 4 pm local time. "
    "A one time equipment allowance of 400 dollars is available every two years. "
    "Security policy. Report lost laptops to the IT desk within 24 hours. "
    "Company laptops must use disk encryption and a screen lock."
)


def test_search_finds_relevant_chunk():
    with Session(engine) as session:
        ingest_text(session, "policy.md", POLICY, size=200, overlap=30)

        relevant = search(session, "How many days do I have to submit receipts?", k=3)
        offtopic = search(session, "What is the capital of France?", k=3)

        print("relevant:", round(relevant[0]["score"], 3), relevant[0]["text"][:70])
        print("off-topic:", round(offtopic[0]["score"], 3), offtopic[0]["text"][:70])

        assert "30 days" in relevant[0]["text"]
        assert relevant[0]["score"] > offtopic[0]["score"]
        session.rollback()