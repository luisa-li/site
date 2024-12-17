import os
import base64
import requests
from fastapi import FastAPI, Response, status 
from dotenv import load_dotenv
from datetime import datetime, timezone

from storage import get_access_key, update_access_key

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_CURRENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"

SCOPE = "user-read-playback-state"

app = FastAPI()

def get_spotify_access_key():
    key, updated_at = get_access_key('spotify')
    updated_at_datetime = datetime.fromisoformat(updated_at).replace(tzinfo=timezone.utc)
    # if access token expired, get another one
    if (datetime.now(timezone.utc) - updated_at_datetime).total_seconds() > 3600:
        key = refresh_key(REFRESH_TOKEN)
        update_access_key("spotify", key)
    return key

def refresh_key(refresh_token):
    url = SPOTIFY_TOKEN_URL
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        new_access_token = tokens.get("access_token")
        return new_access_token
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None
    
@app.get("/listening")
async def get_current_song():
    
    """
    Fetch the currently playing song on Spotify and return an embeddable iframe HTML snippet.
    """
    headers = {
        "Authorization": f"Bearer {get_spotify_access_key()}"
    }
    
    response = requests.get(SPOTIFY_CURRENTLY_PLAYING_URL, headers=headers)
        
    if response.status_code == 200:
        # playing something or it is on pause, either way, return what it is 
        data = response.json() 
        track = data["item"]
        track_id = track["id"]
        embed_url = f"https://open.spotify.com/embed/track/{track_id}"
        
        html_snippet = f"""
        <iframe src="{embed_url}" width="300" height="80" frameborder="0" 
        allowtransparency="true" allow="encrypted-media"></iframe>
        """
        print(html_snippet)
        return Response(content=html_snippet, status_code=status.HTTP_200_OK)
    elif response.status_code == 204:
        # spotify is not open on any of the current devices
        return Response(content=None, status_code=status.HTTP_200_OK)
    else:
        # something went wrong D:
        return Response(content=None, status_code=status.HTTP_400_BAD_REQUEST)
        
