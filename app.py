import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core.models import WorldModel, BlindSpot
from core.engine import analyze_world
from core.extractor import extract_context


logger = logging.getLogger(__name__)


app = FastAPI(
    title="BlindSpot",
    description="An omission detector for plans, commitments, and context.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/dashboard")
def dashboard():
    return FileResponse("static/index.html")

class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text must not be empty or whitespace.")
        return value


@app.get("/")
def root():
    return {
        "name": "BlindSpot",
        "status": "running",
    }


@app.post("/analyze", response_model=list[BlindSpot])
def analyze(world: WorldModel):
    return analyze_world(world)


@app.post("/analyze-text", response_model=list[BlindSpot])
def analyze_text(request: TextRequest):
    try:
        world = extract_context(request.text)
    except Exception as exc:
        logger.exception("Context extraction failed")
        raise HTTPException(
            status_code=502,
            detail="BlindSpot could not analyze this text right now. Please try again.",
        ) from exc

    return analyze_world(world)
