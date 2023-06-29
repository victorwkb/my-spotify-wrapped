import requests

def get_recently_played_data(limit, access_token):
    # define scope and set options
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    params = { 'limit' : limit }
    # make request
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

