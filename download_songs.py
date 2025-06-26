import os
import json
from yt_dlp import YoutubeDL
from datetime import datetime

PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PLxvtIH8nzpyUecs3sbg7ZA1KG6Qco_Uy9'
DOWNLOAD_DIR = 'downloads'
STATIC_DIR = 'app/public/beats'
METADATA_FILE = 'app/public/beats/metadata.json'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Load existing metadata
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
else:
    metadata = {}

def download_new_videos():
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128', 
        }],
        'extract_flat': False,
        'noplaylist': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(PLAYLIST_URL, download=False)
        videos = playlist_info.get('entries', [])

        print(f"Found {len(videos)} videos in playlist.")

        for video in videos:
            if not video or 'id' not in video:
                continue

            video_id = video['id']
            if video_id in metadata:
                print(f"Skipping already downloaded: {video.get('title', 'Unknown')}")
                continue

            print(f"Downloading: {video.get('title', 'Unknown')}")

            try:
                result = ydl.extract_info(video['webpage_url'], download=True)
                filename = f"{video_id}.mp3"
                src = os.path.join(DOWNLOAD_DIR, filename)
                dest = os.path.join(STATIC_DIR, filename)

                if os.path.exists(src):
                    os.rename(src, dest)

                metadata[video_id] = {
                    'id': video_id,
                    'title': result.get('title'),
                    'url': result.get('webpage_url'),
                    'duration': result.get('duration'),
                    'thumbnail': result.get('thumbnail'),
                    'filename': filename,
                    'added': datetime.utcnow().isoformat() + "Z"
                }

                with open(METADATA_FILE, 'w') as f:
                    json.dump(metadata, f, indent=2)

            except Exception as e:
                print(f"Error downloading {video.get('title', video_id)}: {e}")

if __name__ == "__main__":
    download_new_videos()

