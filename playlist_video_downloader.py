import yt_dlp

def download_playlist(playlist_url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',  # Save files in a folder named after the playlist
        'noplaylist': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    url = input("Enter the YouTube playlist URL: ")
    download_playlist(url)