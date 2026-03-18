# FastAPI Calculator

Small FastAPI app with a simple web UI calculator.

## Features
- `GET /` calculator page
- `GET /health` health check
- `POST /add`, `POST /subtract`, `POST /multiply`, `POST /divide`
- Unit, integration, and Playwright end-to-end tests
- GitHub Actions test + container security scan

## Run locally
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `python -m pip install -r requirements.txt`
4. `uvicorn main:app --reload`

Open:
- `http://127.0.0.1:8000/`

## Run with Docker
- `docker compose up --build`

## Tests
- All tests: `python -m pytest -q`
- E2E only: `python -m pytest -q test/test_main_e2e_playwright.py`

If running E2E for the first time:
- `python -m playwright install chromium`
