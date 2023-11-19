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
    
@router.get("/player/{username}/rating-history")
def read_rating_history(username: str, db: Session = Depends(get_db)):
    player = crud.get_player_by_username(db, username)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    rating_history = crud.get_rating_history(db, username)
    if not rating_history:
        raise HTTPException(status_code=404, detail="Rating history not available for the specified player")

    return {"username": username, "rating_history": rating_history}

