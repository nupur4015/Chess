from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.db.models import Player
from app.db.fetch_data import fetch_top_players_data
from app.db.store_data import store_top_players_data
from app.api import players


app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(players.router)

# Endpoint to fetch and store top players data
@app.get("/fetch-top-players")
def fetch_top_players(db: Session = Depends(get_db)):
    try:
        # Fetch top players data
        top_players_data = fetch_top_players_data()

        # Store top players data in the database
        store_top_players_data(db, top_players_data)

        return {"message": "Top players data fetched and stored successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
