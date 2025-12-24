# app/schemas/response.py
from pydantic import BaseModel
from typing import Optional

class InferenceResponse(BaseModel):
    status: str
    probability: float
    advice: str
    image_url: Optional[str] = None