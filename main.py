from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp
import time
import logging
import zipfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)

def download_playlist(playlist_url: str):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',
        'noplaylist': False,
        'ratelimit': '500K',
        'progress_hooks': [hook]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return {"status": "error", "message": str(e)}

def hook(d):
    if d['status'] == 'downloading':
        logging.info(f"Downloading: {d['filename']} ({d['downloaded_bytes']} bytes downloaded)")

@app.post("/download/")
async def download(playlist_url: str = Form(...)):
    try:
        # Create a directory for the playlist if it doesn't exist
        playlist_name = playlist_url.split("list=")[-1]
        os.makedirs(playlist_name, exist_ok=True)

        # Download the playlist
        download_playlist(playlist_url)

        # Create a ZIP file after downloading all videos
        zip_filename = f"{playlist_name}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(playlist_name):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        time.sleep(1)  # Sleep to reduce detection
        return {"status": "success", "message": "Playlist download started", "zip_file": zip_filename}
    except Exception as e:
        logging.error(f"Endpoint error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/download-zip/{zip_filename}")
async def download_zip(zip_filename: str):
    return FileResponse(zip_filename)

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content
