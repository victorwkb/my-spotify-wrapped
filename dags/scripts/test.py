from spotify_auth import get_spotify_auth_url, exchange_code_for_tokens, handle_callback, refresh_access_token
import json
import os
import dotenv
import requests

dotenv.load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
spotify_email = os.getenv("SPOTIFY_EMAIL")
spotify_password = os.getenv("SPOTIFY_PASSWORD")

# Spotify Authorization Code Flow

auth_url, state = get_spotify_auth_url(client_id, redirect_uri)

code, state = handle_callback(auth_url, redirect_uri, spotify_email, spotify_password)

access_token, refresh_token = exchange_code_for_tokens(code, client_id, client_secret, redirect_uri, state)

access_token = refresh_access_token(refresh_token, client_id, client_secret)
print("refresh token success")

new_refreshed_token = refresh_access_token(refresh_token, client_id, client_secret)
print("refreshed token for the second time success!")

api_url = "https://api.spotify.com/v1/me/player/recently-played"
headers = {
    "Authorization": 'Bearer ' + access_token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}
params = { 'limit' : 1 }

def make_authorized_get_request(api_url, headers, params):
    response = requests.get(url=api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error')

data = make_authorized_get_request(api_url, headers, params)

json_str = json.dumps(data, indent=4)
print(json_str)
