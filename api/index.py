import os
import base64
import requests
from fastapi import FastAPI, Response, status 
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from datetime import datetime, timezone
from api.storage import get_access_key, update_access_key
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_CURRENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"

SCOPE = "user-read-playback-state"

app = FastAPI()

origins = [
    "https://luisali.com", 
    "https://*.vercel.app",  
    "http://127.0.0.1:5500/*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"], 
)

def get_spotify_access_key():
    # Your logic to get the access key
    key, updated_at = get_access_key('spotify')
    updated_at_datetime = datetime.fromisoformat(updated_at).replace(tzinfo=timezone.utc)
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
        return tokens.get("access_token")
    else:
        return None

@app.get("/listening")
async def get_current_song():
    headers = {
        "Authorization": f"Bearer {get_spotify_access_key()}"
    }
    response = requests.get(SPOTIFY_CURRENTLY_PLAYING_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        track = data.get("item")
        is_playing = data.get("is_playing", False)  # Default to False if not present

        if track and is_playing:
            track_id = track.get("id")
            embed_url = f"https://open.spotify.com/embed/track/{track_id}"
            html_snippet = f"""
            <iframe src="{embed_url}" width="300" height="80" frameborder="0" 
            allowtransparency="true" allow="encrypted-media"></iframe>
            """
        return Response(content=html_snippet, status_code=status.HTTP_200_OK)
    elif response.status_code == 204:
        return Response(content=None, status_code=status.HTTP_200_OK)
    else:
        return Response(content=None, status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/{file_name}")
async def serve_static_files(file_name: str):
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}