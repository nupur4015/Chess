from app.lichess.client import get_rating_history
from sqlalchemy.orm import Session
from app.db.models import Player
from datetime import datetime
import json
from sqlalchemy.exc import SQLAlchemyError
import time

def store_top_players_data(db: Session, top_players_data):
    # Check if top_players_data is a dictionary and contains the 'users' key
    if isinstance(top_players_data, dict) and 'users' in top_players_data:
        # Extract the 'users' list from top_players_data
        users_data = top_players_data['users']

        # Retry up to 3 times if a transaction fails
        for retry in range(3):
            try:
                # Begin a new transaction
                with db.begin():
                    # Iterate through the users data and store it in the database
                    for index, user_data in enumerate(users_data, start=1):
                        # Check if user_data is a dictionary and contains the 'username' key
                        if isinstance(user_data, dict) and 'username' in user_data:
                            username = user_data['username']

                            try:
                                print(f"Fetching index for username: {index}")
                                rating_history = get_rating_history(username)

                                # Convert datetime objects to strings
                                for entry in rating_history:
                                    entry['date'] = entry['date'].isoformat()

                                # Check if the player already exists in the database
                                existing_player = db.query(Player).filter(Player.username == username).first()

                                if existing_player:
                                    # Update the existing player's rating history
                                    existing_player.rating_history = json.dumps(rating_history)
                                    existing_player.serial_number = index
                                else:
                                    # Create a new player entry in the database
                                    new_player = Player(
                                        username=username,
                                        rating_history=json.dumps(rating_history),
                                        serial_number=index,
                                    )
                                    db.add(new_player)

                            except Exception as e:
                                print(f"Error getting rating history for {username}: {e}")

                # Commit the changes to the database
                db.commit()

                # Break out of the retry loop if successful
                break

            except SQLAlchemyError as e:
                print(f"Error during transaction: {e}")
                # Check if the error is a unique constraint violation
                if "duplicate key value violates unique constraint" in str(e):
                    print(f"Player with username {username} already exists. Updating the existing record.")
                    # Handle the unique constraint violation by updating the existing record
                    existing_player = db.query(Player).filter(Player.username == username).first()
                    existing_player.rating_history = json.dumps(rating_history)
                    existing_player.serial_number = index
                    # Commit the changes within the same transaction
                    db.commit()
                    break

                # Wait for a short duration before retrying
                time.sleep(1)


