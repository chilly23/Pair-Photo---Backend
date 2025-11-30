# Pair Programming Prototype (No Docker required)

This project is a minimal, full-stack pair-programming demo. Two users can join the same room and edit a shared editor in real time. The server persists room state and exposes a mocked autocomplete endpoint.

## What is included
- Backend: FastAPI, WebSocket, SQLite by default, SQLAlchemy.
- Frontend: React + TypeScript minimal client with a simple editor and autocomplete UI.

## Why this layout
- SQLite default so you can run locally without installing Postgres.
- Clear module separation: routers, crud, models, ws manager.
- WebSocket uses a connection manager for broadcasting.

---

## Quick start on Windows (no Docker)

### Prerequisites
- Python 3.8+ (Install from python.org; check `python --version`)
- Node 16+ and npm (for frontend)
- optional: git

### Backend
1. Open cmd in `pair-proto/backend`:
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
