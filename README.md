# 🎸 RockVault

A personal web app to download and back up rock music from YouTube as MP3 files.

Built as a learning project covering full-stack web development,
HTTP fundamentals, and application security.

## Tech Stack

- **Backend:** Python 3 + FastAPI
- **Downloader:** yt-dlp + FFmpeg
- **Frontend:** HTML/CSS/JS (planned)
- **Server:** Ubuntu Server 24 (headless)
- **Version Control:** Git + GitHub

## Project Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | FastAPI running, base structure | ✅ Done |
| Phase 2 | yt-dlp integration, download pipeline | ✅ Done |
| Phase 3 | Frontend UI connected to backend | 🔄 In progress |
| Phase 4 | HTTP deep dive, Swagger, logs | ⏳ Planned |
| Phase 5 | Security audit and hardening | ⏳ Planned |

## Features

- `POST /download` — Accepts a YouTube URL and downloads the audio as MP3
- `GET /files` — Returns a list of all downloaded MP3 files
- `GET /health` — Health check endpoint
- `GET /docs` — Interactive API documentation (Swagger UI)

## Running Locally
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

## Project Structure
```
RockVault/
├── backend/
│   ├── __init__.py
│   └── main.py
├── frontend/          # Planned — Phase 3
├── downloads/         # MP3 files (not tracked by Git)
├── docs/
│   └── linkedin-plan.md
└── README.md
```

## Security Notes

This project intentionally explores application security as a learning goal.
Vulnerabilities found during development are documented in `docs/security-audit.md` (Phase 5).