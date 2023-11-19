from app.lichess.client import get_top_players, get_rating_history

def fetch_top_players_data():
    # Fetch data on the top 500 classical chess players
    top_players_data = get_top_players()

    return top_players_data
