# BlindSpot

**Find the problems your plan forgot to account for.**

BlindSpot is a prototype omission-detection tool designed to identify hidden commitments, scheduling conflicts, and missing prerequisites in a user's plans.

## What it does

- **Ghost Commitments:** surfaces commitments that may be forgotten.
- **Temporal Collisions:** identifies potential scheduling conflicts.
- **Prerequisite Failures:** flags steps that may be missing before a planned task can succeed.
- **Actionable findings:** presents detected issues and suggested next steps through a web dashboard.

## Technology

- Python and FastAPI
- HTML, CSS, and JavaScript
- Pytest

## Run locally

1. Clone this repository and enter the project directory.
2. Create and activate a Python virtual environment.
3. Install the dependencies.
4. Start the application.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open http://127.0.0.1:8000/dashboard in your browser.

## Run tests

```bash
pytest -q
```

## API

The text-analysis endpoint is:

`POST /analyze-text`

Use the running application's API documentation at http://127.0.0.1:8000/docs to inspect the available request format.

## Project status

BlindSpot is a hackathon prototype. Detection results should be reviewed by the user; they are not a guarantee that every conflict or omission will be found.

## Security

Never commit API keys, `.env` files, credentials, or private keys. Configure any required provider credentials locally.

# blindspot
 aaa29a927525ea6e109a6c7e7f1d936d54a28edb
