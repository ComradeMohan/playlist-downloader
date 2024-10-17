from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import shutil
import zipfile
from uuid import uuid4

app = FastAPI()

# CORS middleware to allow access from any origin, can limit origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to download YouTube playlist and store videos in a temporary folder
def download_playlist(playlist_url: str):
    temp_folder = str(uuid4())  # Unique folder for each download
    os.makedirs(temp_folder, exist_ok=True)
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{temp_folder}/%(title)s.%(ext)s',  # Save videos in the temporary folder
        'noplaylist': False,  # Ensure full playlist download
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])
    
    return temp_folder  # Return the folder where videos are saved

# Function to zip all videos in a folder
def zip_videos(folder_path: str):
    zip_filename = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=file)  # Add file to zip archive
    return zip_filename

# Endpoint to handle playlist download
@app.post("/download/")
async def download(playlist_url: str = Form(...)):
    try:
        # Step 1: Download the playlist
        download_folder = download_playlist(playlist_url)

        # Step 2: Zip the downloaded videos
        zip_filepath = zip_videos(download_folder)

        # Step 3: Clean up the original download folder
        shutil.rmtree(download_folder)

        # Step 4: Return the ZIP file to the user
        return FileResponse(path=zip_filepath, filename=f"{os.path.basename(zip_filepath)}", media_type='application/zip')

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Route to serve HTML form (index.html)
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content

# Command to start the server: uvicorn main:app --reload
