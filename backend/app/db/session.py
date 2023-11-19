# backend/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://sahxuxoo:sJ4QmF2NkNXHq6Gn4nTDrW8qRxMeP02S@bubble.db.elephantsql.com/sahxuxoo"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
