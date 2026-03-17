"""
RockVault Backend — Main Application Entry Point

This module initializes the FastAPI application and defines the core routes,
including the MP3 download pipeline powered by yt-dlp and FFmpeg.
"""

import yt_dlp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

# --- App Configuration ---

DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="RockVault API",
    description="Backend API for RockVault — a personal rock music backup tool.",
    version="0.2.0",
)

# --- Request Schema ---

class DownloadRequest(BaseModel):
    """
    Schema for the download endpoint request body.

    Attributes:
        url: A valid YouTube video or playlist URL.
    """
    url: str


# --- Routes ---

@app.get("/health", tags=["System"])
def health_check():
    """
    Health Check Endpoint

    Returns the current status of the API.
    Used to verify that the server is running and reachable.
    """
    return {"status": "ok", "message": "RockVault is alive 🎸"}


@app.post("/download", tags=["Downloads"])
def download_mp3(request: DownloadRequest):
    """
    MP3 Download Endpoint

    Accepts a YouTube URL and downloads the audio as an MP3 file
    into the downloads/ directory using yt-dlp and FFmpeg.

    Args:
        request: A DownloadRequest object containing the target URL.

    Returns:
        A JSON response with the status and output filename.

    Raises:
        HTTPException 400: If yt-dlp fails to process the URL.
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            filename = ydl.prepare_filename(info)
            # The actual file will have .mp3 extension after conversion
            mp3_filename = Path(filename).stem + ".mp3"
            return {
                "status": "success",
                "file": mp3_filename,
            }
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))
