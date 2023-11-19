# backend/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

DATABASE_URL = "postgresql://iatgtorl:rqee6vQ-A5dTA1uv9cuXlphrWxolS8TL@bubble.db.elephantsql.com/iatgtorl"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
