from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Player



def get_top_classical_players(db, limit=50, rating_history='Classical'):
    query = (
        db.query(Player.username)
        .order_by(Player.serial_number)
        .limit(limit)
    )
    result = query.all()
    return [username for (username,) in result]

def get_player_by_username(db: Session, username: str):
    return db.query(Player).filter(Player.username == username).first()

def get_rating_history(db: Session, username: str, days: int = 30):
    
    player = get_player_by_username(db, username)
    if player:
        return player.rating_history
    return None