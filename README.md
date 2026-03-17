# 🎸 RockVault

A personal web app to download and back up rock music from YouTube as MP3 files.

Built as a learning project covering full-stack web development, HTTP fundamentals, and application security.

## Tech Stack

- **Backend:** Python 3 + FastAPI
- **Downloader:** yt-dlp + FFmpeg
- **Frontend:** HTML/CSS/JS (planned)
- **Server:** Ubuntu Server (headless)
- **Version Control:** Git + GitHub

## Project Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | FastAPI running, base structure | ✅ In progress |
| Phase 2 | yt-dlp integration, download pipeline | ⏳ Planned |
| Phase 3 | Frontend UI connected to backend | ⏳ Planned |
| Phase 4 | HTTP deep dive, Swagger, logs | ⏳ Planned |
| Phase 5 | Security audit and hardening | ⏳ Planned |

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
