import requests
import base64
import string
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode, urlparse, parse_qs

# dotenv.load_dotenv()
# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
# redirect_uri = os.getenv("REDIRECT_URI")
# spotify_email = os.getenv("SPOTIFY_EMAIL")
# spotify_password = os.getenv("SPOTIFY_PASSWORD")

# Spotify Authorization Code Flow

def get_spotify_auth_url(client_id, redirect_uri):
    letters = string.ascii_letters + string.digits
    state = ''.join(random.choice(letters) for _ in range(16))
    auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
        'response_type': "code",
        'client_id': client_id,
        'scope': "user-read-recently-played",
        'redirect_uri': redirect_uri,
        'state': state
    })
    return auth_url, state

def handle_callback(auth_url, redirect_uri, spotify_email, spotify_password):
    # firefox webdriver
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
    driver.get(auth_url)
    
    # login to spotify
    email_field = driver.find_element(By.ID, 'login-username')
    email_field.send_keys(spotify_email)
    password_field = driver.find_element(By.ID, 'login-password')
    password_field.send_keys(spotify_password)
    password_field.send_keys(Keys.RETURN)

    # wait for redirect and get url
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains(redirect_uri))
    callback_url = driver.current_url

    # parse url for code and state
    parsed = urlparse(callback_url)
    query_params = parse_qs(parsed.query)
    code = query_params["code"][0]
    state = query_params["state"][0]

    driver.quit()
    return code, state


def exchange_code_for_tokens(code, client_id, client_secret, redirect_uri, state):
    # configure auth message format according to spotify
    message = f"{client_id}:{client_secret}"
    message_bin = message.encode('utf-8')
    b64_bin = base64.b64encode(message_bin)
    b64_message = b64_bin.decode('utf-8')
    auth_message = f"Basic {b64_message}"
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
            'state': state
        },
        'headers': {
            'Authorization': auth_message,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }
    # exchange code for tokens
    response = requests.post(url=auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        return access_token, refresh_token
    else:
        raise Exception(f"Failed to exchange code for tokens", response.status_code)

def refresh_access_token(refresh_token, client_id, client_secret):
    message = f"{client_id}:{client_secret}"
    message_bin = message.encode('utf-8')
    b64_bin = base64.b64encode(message_bin)
    b64_message = b64_bin.decode('utf-8')
    auth_message = f"Basic {b64_message}"
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
            },
        'headers': {
            'Authorization': auth_message,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }
    # request new access token
    response = requests.post(auth_options["url"], data=auth_options["data"], headers=auth_options["headers"])
    if response.status_code == 200:
        data = response.json()
        print(data)
        refreshed_token = data["access_token"]
        return refreshed_token
    else:
        raise Exception(f"Failed to refresh access token", response.status_code)

