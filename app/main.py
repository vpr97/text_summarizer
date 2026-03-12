from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # FIX #2

from pydantic import BaseModel, validator
from app.summarizer import summarize_text

app = FastAPI(title="Text Summarizer API", version="1.0")

# Streamlit (8501) → FastAPI (8000) is cross-origin; CORS is required

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 130
    min_length: int = 30

    # Validating before the model even runs

    @validator("text")

    def text_not_empty(cls, v):

        if not v.strip(): raise ValueError("Text cannot be empty.")

        return v


    @validator("min_length")

    def min_lt_max(cls, v, values):

        if "max_length" in values and v >= values["max_length"]:

            raise ValueError("min_length must be less than max_length.")

        return v


class SummarizeResponse(BaseModel):
    summary: str

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    try:
        summary = summarize_text(request.text, request.max_length, request.min_length)
        return SummarizeResponse(summary=summary)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")