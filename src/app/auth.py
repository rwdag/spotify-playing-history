import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = 'user-read-currently-playing'
BASE_AUTH_URL = 'https://accounts.spotify.com/authorize'
AUTH_URL = f'{BASE_AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}'

def get_token(code: str) -> dict:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    tokens = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
    return tokens

def refresh_token(refresh_token: str) -> dict:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    tokens = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
    return tokens