import os
from typing import TypedDict, Any

import requests


class Prediction(TypedDict):
    label: str
    confidence: float
    celiac_risk: str
    contains_gluten: bool | None
    notes: str
    server_questions: list[str]


class ApiResult(TypedDict):
    filename: str | None
    predictions: list[Prediction]


API_BASE_URL = os.getenv("GLUTEN_GUARD_API_URL", "http://localhost:8000")
PREDICT_URL = f"{API_BASE_URL.rstrip('/')}/predict"


def _read_image_bytes(image_input: Any) -> tuple[bytes, str]:
    """Extract raw bytes and a filename from a Streamlit UploadedFile or a SampleFile."""
    if hasattr(image_input, "getvalue"):
        return image_input.getvalue(), image_input.name
    if hasattr(image_input, "read"):
        return image_input.read(), getattr(image_input, "name", "image.jpg")
    if hasattr(image_input, "path"):
        with open(image_input.path, "rb") as f:
            return f.read(), image_input.name
    raise ValueError("Unsupported image input type")


def call_gluten_guard_api(image_input: Any = None) -> ApiResult:
    """
    Upload an image to the GlutenGuard API and return the parsed response.

    The API returns:
      - filename: str | None
      - predictions: list of predictions, each containing:
          label, confidence, celiac_risk, contains_gluten, notes, server_questions
    """
    raw_bytes, filename = _read_image_bytes(image_input)

    try:
        resp = requests.post(
            PREDICT_URL,
            files={"file": (filename, raw_bytes)},
            timeout=(5, 60),
        )
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Could not connect to the GlutenGuard API at {PREDICT_URL}.\n"
            f"Make sure the API is running (e.g. `uvicorn api.fast:app --reload --port 8000`)."
        )
    return resp.json()
