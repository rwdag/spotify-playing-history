import requests
from time import sleep, time
from datetime import datetime

from app.auth import refresh_token
from db.database import insert_track


def get_current_track(access_token: str) -> dict:
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    
    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    req = requests.get(url, headers=headers)
    if req.status_code != 200:          # No data from API
        return None

    parsed_req = req.json()
    if not parsed_req['is_playing']:    # Current track is stopped/not playing 
        return None
    
    try:
        track = parsed_req['item']
        track = {'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'featured_artists': ', '.join([artist['name'] for i, artist in enumerate(track['artists']) if i > 0]) or None,
                'duration_ms': track['duration_ms'],
                'release_date': track['album']['release_date'],
                'popularity': track['popularity']}
        return track
    except TypeError:       # to treat edge cases where parsed_req has no 'item' key as if no data was sent by API
        return None


# Logic that checks the current song's playback status and returns timing metadata accordingly
def check_song_status(start: int, current_track: str, previous_track: str) -> tuple:
    if not previous_track and previous_track != current_track:  # song started
        new_start = time()
        return current_track, 0, new_start
    
    if previous_track and previous_track != current_track:  # song changed
        time_played = time() - start
        new_start = time()
        return previous_track, time_played, new_start

    if previous_track == current_track:     #song is playing
        return current_track, 0, start
    

def main_loop(tokens: dict, refresh: str) -> None:
    # Init song status variables
    previous_track = None
    song_start = time()

    while True:
        token_start = time()

        while time() + 10  < token_start + tokens['expires_in']:  #refreshing token 10s before it expires
            track = get_current_track(tokens['access_token'])
            previous_track, time_played, song_start = check_song_status(song_start, track, previous_track)

            if time_played and previous_track != track:     # song changed or stopped
                previous_track['started_at'] = str(datetime.fromtimestamp(time()-time_played))
                previous_track['ms_played'] = int(time_played*1000)
                insert_track(previous_track)
                previous_track = track      # move to curretly playing song

            sleep(0.2)
        tokens = refresh_token(refresh)