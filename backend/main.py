"""
RockVault Backend — Main Application Entry Point

This module initializes the FastAPI application, database models,
and core routes including the MP3 download pipeline and download history.
"""

import re
from datetime import datetime
from pathlib import Path

import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

# --- Database Configuration ---

DATABASE_URL = "sqlite:///./rockvault.db"
engine = create_engine(DATABASE_URL)


class DownloadRecord(SQLModel, table=True):
    """
    Database model for a completed download.

    Attributes:
        id: Auto-incremented primary key.
        title: The filename of the downloaded MP3.
        downloaded_at: Timestamp of when the download completed.
    """
    id: int | None = Field(default=None, primary_key=True)
    title: str
    downloaded_at: datetime = Field(default_factory=datetime.utcnow)


def init_db():
    """Creates database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


# --- App Configuration ---

DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="RockVault API",
    description="Backend API for RockVault — a personal rock music backup tool.",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@app.on_event("startup")
def on_startup():
    """Initializes the database on application startup."""
    init_db()


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
    """
    return {"status": "ok", "message": "RockVault is alive 🎸"}


@app.post("/download", tags=["Downloads"])
def download_mp3(request: DownloadRequest):
    """
    MP3 Download Endpoint

    Accepts a YouTube URL, downloads the audio as MP3, saves a record
    to the database, and returns the file for the client to download.
    The file is deleted from the server after being served.

    Args:
        request: A DownloadRequest object containing the target URL.

    Returns:
        The MP3 file as a downloadable response.

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
            filename = Path(ydl.prepare_filename(info)).stem + ".mp3"
            file_path = DOWNLOADS_DIR / filename

            # Save record to database
            with Session(engine) as session:
                record = DownloadRecord(title=filename)
                session.add(record)
                session.commit()

            # Serve file and delete after response
            return FileResponse(
                path=file_path,
                media_type="audio/mpeg",
                filename=filename,
                headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
            )

    except yt_dlp.utils.DownloadError as e:
        clean_message = re.sub(r'\x1b\[[0-9;]*m', '', str(e)).strip()
        raise HTTPException(status_code=400, detail=f"Download failed: {clean_message}")
    except yt_dlp.utils.ExtractorError as e:
        raise HTTPException(status_code=422, detail=f"Could not extract video info: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/history", tags=["Downloads"])
def get_history():
    """
    Download History Endpoint

    Returns a list of all previously downloaded files from the database,
    ordered by most recent first.

    Returns:
        A JSON response with the total count and list of download records.
    """
    with Session(engine) as session:
        records = session.exec(
            select(DownloadRecord).order_by(DownloadRecord.downloaded_at.desc())
        ).all()

        return {
            "total": len(records),
            "history": [
                {
                    "id": r.id,
                    "title": r.title,
                    "downloaded_at": r.downloaded_at.strftime("%Y-%m-%d %H:%M")
                }
                for r in records
            ]
        }


@app.delete("/history/{record_id}", tags=["Downloads"])
def delete_record(record_id: int):
    """
    Delete History Record Endpoint

    Removes a specific record from the download history.

    Args:
        record_id: The ID of the record to delete.

    Raises:
        HTTPException 404: If the record does not exist.
    """
    with Session(engine) as session:
        record = session.get(DownloadRecord, record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found.")
        session.delete(record)
        session.commit()
        return {"status": "deleted", "id": record_id}