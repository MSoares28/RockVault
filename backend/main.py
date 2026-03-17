"""
RockVault Backend — Main Application Entry Point

This module initializes the FastAPI application and defines the core routes,
including the MP3 download pipeline powered by yt-dlp and FFmpeg.
"""

import re
import yt_dlp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

# --- App Configuration ---

DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="RockVault API",
    description="Backend API for RockVault — a personal rock music backup tool.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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
            mp3_filename = Path(filename).stem + ".mp3"
            return {
                "status": "success",
                "file": mp3_filename,
            }
    except yt_dlp.utils.DownloadError as e:
        clean_message = re.sub(r'\x1b\[[0-9;]*m', '', str(e)).strip()
        raise HTTPException(status_code=400, detail=f"Download failed: {clean_message}")
    except yt_dlp.utils.ExtractorError as e:
        raise HTTPException(status_code=422, detail=f"Could not extract video info: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/files", tags=["Downloads"])
def list_files():
    """
    List Downloaded Files Endpoint

    Returns a list of all MP3 files currently stored in the downloads/ directory.

    Returns:
        A JSON response with the total file count and a list of filenames.
    """
    files = sorted(DOWNLOADS_DIR.glob("*.mp3"))
    return {
        "total": len(files),
        "files": [f.name for f in files],
    }
