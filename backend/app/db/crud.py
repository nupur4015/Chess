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