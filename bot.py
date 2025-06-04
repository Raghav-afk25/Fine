from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from yt_dlp import YoutubeDL
import os, uuid

app = FastAPI()
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.post("/download")
async def download(query: str = Form(...)):
    file_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"
    final_path = f"{DOWNLOAD_DIR}/{file_id}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
        return {
            "status": "success",
            "title": info.get("title"),
            "url": f"http://YOUR_VPS_IP:8000/downloads/{file_id}.mp3"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/downloads", StaticFiles(directory=DOWNLOAD_DIR), name="downloads")
