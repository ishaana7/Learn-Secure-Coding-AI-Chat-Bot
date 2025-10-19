import os
import requests
from typing import Optional

# ----------------------------
# Gemma API key and endpoint
# ----------------------------
GEMMA_API_KEY = "AIzaSyAip6sQ25rGgEOYpJcGdehOAkOFO91mjUw"  # <-- PUT YOUR KEY HERE
GEMMA_URL = "http://localhost:11434/api/generate"
# ----------------------------


def get_response(prompt: str) -> str:
    """Send a prompt to Gemma and return the response text."""
    if not GEMMA_API_KEY or GEMMA_API_KEY.strip() == "":
        return "❌ Gemma API key not set."

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMMA_API_KEY,
    }

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        resp = requests.post(GEMMA_URL, headers=headers, json=data, timeout=20)
        resp.raise_for_status()
        result = resp.json()
        return (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
            or "⚠️ No response from Gemma."
        )
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
