
from fastapi import FastAPI, Form
from pydantic import BaseModel
import yt_dlp
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, but you can specify specific ones
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

def download_playlist(playlist_url: str):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',  # Save files in a folder named after the playlist
        'noplaylist': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

@app.post("/download/")
async def download(playlist_url: str = Form(...)):
    try:
        download_playlist(playlist_url)
        return {"status": "success", "message": "Playlist download started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Start the server with: uvicorn main:app --reload
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content




