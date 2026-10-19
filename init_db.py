from sqlalchemy import text

from db import engine
from models import Base

with engine.begin() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

Base.metadata.create_all(engine)
print("tables ready")