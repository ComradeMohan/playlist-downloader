from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import yt_dlp
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_playlist(playlist_url: str):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',
        'noplaylist': False,
        'ratelimit': '500K',  # Adjust the rate limit as needed
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/download/")
async def download(playlist_url: str = Form(...)):
    try:
        download_playlist(playlist_url)
        time.sleep(1)  # Sleep between downloads to reduce detection
        return {"status": "success", "message": "Playlist download started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content
