# top_players.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud
from app.db.session import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/top-players")
def get_top_classical_players(db: Session = Depends(get_db)):
    players = crud.get_top_classical_players(db)
    return players


