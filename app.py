from fastapi import FastAPI
from pydantic import BaseModel

from core.models import WorldModel, BlindSpot
from core.engine import analyze_world
from core.extractor import extract_context


app = FastAPI(
    title="BlindSpot",
    description="An omission detector for plans, commitments, and context.",
    version="0.1.0",
)


class TextRequest(BaseModel):
    text: str


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
    world = extract_context(request.text)
    return analyze_world(world)
