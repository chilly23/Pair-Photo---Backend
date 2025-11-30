@echo off
REM activate venv if present
if exist .venv\Scripts\activate (
  call .venv\Scripts\activate
)

REM set SQLite default; if you want Postgres set DATABASE_URL env
if "%DATABASE_URL%"=="" (
  echo Using default sqlite dev.db. To override set DATABASE_URL.
)

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
