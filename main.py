from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import yt_dlp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_playlist(playlist_url: str, cookies_file: str = None):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',
        'noplaylist': False,
        'cookiefile': cookies_file  # Use a cookie file if needed
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

@app.post("/download/")
async def download(playlist_url: str = Form(...), cookies_file: str = Form(None)):
    try:
        download_playlist(playlist_url, cookies_file)
        return {"status": "success", "message": "Playlist download started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content

# Start the server with: uvicorn main:app --reload
