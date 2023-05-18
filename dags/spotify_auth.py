import requests
import base64
import os
import string
import random
from urllib.parse import urlencode

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
state_key = "spotify_auth_state"

# Spotify Authorization Code Flow

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def get_spotify_auth_url():
    state = generate_random_string(16)
    auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
        "response_type": "code",
        "client_id": client_id,
        "scope": "user-read-recently-played",
        "redirect_uri": redirect_uri,
        "state": state
    })
    return auth_url, state

def exchange_code_for_tokens(code, state):
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        },
        'headers': {
            'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
        }
    }

    response = requests.post(auth_options["url"], data=auth_options["data"], headers=auth_options["headers"])
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        return access_token, refresh_token
    else:
        raise Exception("Failed to exchange code for tokens")

def refresh_access_token(refresh_token):
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
        },
        'data': {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    }

    response = requests.post(auth_options["url"], data=auth_options["data"], headers=auth_options["headers"])
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        return access_token
    else:
        raise Exception("Failed to refresh access token")

