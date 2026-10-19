from fastapi import Depends, FastAPI, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from db import engine
from ingest import ingest_text
from search import retrieve

MAX_UPLOAD_BYTES = 5 * 1024 * 1024

app = FastAPI(title="Atlas AI")


def get_session():
    with Session(engine) as session:
        yield session


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/name")
def name():
    return {"name": "Atlas AI"}


@app.post("/documents")
def upload_document(file: UploadFile, session: Session = Depends(get_session)):
    filename = file.filename or ""
    if not filename.lower().endswith((".md", ".txt")):
        raise HTTPException(400, "Only .md and .txt files are supported for now")
    raw = file.file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File is too large (limit 5 MB)")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be UTF-8 text")
    try:
        doc, created = ingest_text(session, filename, text)
    except ValueError as error:
        raise HTTPException(400, str(error))
    session.commit()
    return {"document_id": doc.id, "filename": doc.filename, "created": created}


@app.post("/ask")
def ask(body: AskRequest, session: Session = Depends(get_session)):
    return retrieve(session, body.question)