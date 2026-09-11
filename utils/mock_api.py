import requests
from typing import TypedDict, Any


class ApiResult(TypedDict):
    risk_score: int
    text: str


API_URL = "http://127.0.0.1:8000"


def call_gluten_guard_api(image_input: Any = None) -> ApiResult:
    """Send an image to the prediction API and return the identified dish.

    NOTE: risk_score is a placeholder (always 0). The model identifies dishes,
    it does not assess gluten content. The dish-to-risk mapping is still open.
    """
    if hasattr(image_input, "getvalue"):
        name, content = image_input.name, image_input.getvalue()
    elif hasattr(image_input, "path"):
        name = image_input.name
        content = open(image_input.path, "rb").read()
    else:
        return {"risk_score": 0, "text": "### No image provided"}

    try:
        response = requests.post(
            f"{API_URL}/predict",
            files={"file": (name, content, "image/jpeg")},
            params={"top_k": 5},
            timeout=60,
        )
        response.raise_for_status()
        predictions = response.json()["predictions"]
    except requests.RequestException as err:
        return {
            "risk_score": 0,
            "text": (
                "### Could not reach the prediction service\n\n"
                f"`{err}`\n\n"
                f"Is the API running at `{API_URL}`?"
            ),
        }

    top = predictions[0]

    lines = [
        f"### Identified Dish: **{top['label'].replace('_', ' ').title()}**",
        "",
        f"**Model confidence:** {top['confidence'] * 100:.1f}%",
        "",
        "#### Other candidates:",
    ]
    for p in predictions[1:]:
        lines.append(f"- {p['label'].replace('_', ' ').title()} — {p['confidence'] * 100:.1f}%")

    lines += [
        "",
        "---",
        "",
        "> ⚠️ **Gluten risk assessment not implemented yet.**",
        "> The score shown above is a placeholder and carries no meaning.",
        "> The model only identifies the dish — it does not assess gluten content.",
        "> Mapping from dish to gluten risk is still open.",
    ]

    return {
        "risk_score": 0,
        "text": "\n".join(lines),
    }
