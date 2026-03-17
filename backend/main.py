"""
RockVault Backend — Main Application Entry Point

This module initializes the FastAPI application and defines the core routes.
"""

from fastapi import FastAPI

app = FastAPI(
    title="RockVault API",
    description="Backend API for RockVault — a personal rock music backup tool.",
    version="0.1.0",
)


@app.get("/health", tags=["System"])
def health_check():
    """
    Health Check Endpoint

    Returns the current status of the API.
    Used to verify that the server is running and reachable.
    """
    return {"status": "ok", "message": "RockVault is alive 🎸"}
