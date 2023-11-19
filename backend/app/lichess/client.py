from requests.exceptions import RequestException
import requests  

def get_top_players(limit=500):
    try:
        url = f"https://lichess.org/api/player/top/{limit}/classical"
        #params = {"nb": limit, "perf": "classical"}

        response = requests.get(url)
        response.raise_for_status()

        return response.json()
    except RequestException as e:
        print(f"Error in get_top_players: {e}")
        raise

from datetime import datetime, timedelta

import requests
from datetime import datetime, timedelta

def get_rating_history(username):
    url = f"https://lichess.org/api/user/{username}/rating-history"

    try:
        response = requests.get(url)
        response.raise_for_status()

        rating_history = []
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        for perf_type in response.json():
            if isinstance(perf_type, dict) and "points" in perf_type:
                name = perf_type.get("name")
                points = perf_type.get("points")
                print(f"{name}")
                # Check if the perf_type is "classical" Sand process its points
                if name == "Classical":
                    for entry in points:
                        if isinstance(entry, list) and len(entry) == 4:
                            year, month, day, rating = entry
                            date = datetime(year, month + 1, day)  # Adjust month to start from 1

                            # Only consider entries from the last 30 days
                            if date >= thirty_days_ago:
                                rating_history.append({"perf_type": name, "date": date, "rating": rating})
                        else:
                            print(f"Ignoring unexpected entry format: {entry}")

        return rating_history
    except requests.exceptions.RequestException as e:
        print(f"Error in get_rating_history: {e}")
        return None
