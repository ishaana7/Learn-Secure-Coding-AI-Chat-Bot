"""
Simple AI client wrapper with flexible provider selection.

This module supports two providers by default:
 - openai: uses OpenAI Chat Completions (OPENAI_API_KEY required)
 - gemma: a generic HTTP endpoint (GEMMA_URL and GEMMA_API_KEY expected)

Configure which provider to use with the environment variable AI_PROVIDER.
Examples (macOS / zsh):

  export AI_PROVIDER=gemma
  export GEMMA_URL="https://gemma.example.com/v1/generate"
  export GEMMA_API_KEY="your_gemma_key"

If no provider is set, the module defaults to "openai" and expects OPENAI_API_KEY.
"""

import os
import json
import requests
from typing import Optional


AI_PROVIDER = os.environ.get("AI_PROVIDER", "openai").lower()

# OpenAI settings (used when AI_PROVIDER == 'openai')
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Gemma settings (used when AI_PROVIDER == 'gemma')
GEMMA_URL = os.environ.get("GEMMA_URL")
GEMMA_API_KEY = os.environ.get("GEMMA_API_KEY")


def set_gemma_api_key(key: str):
    """Set the Gemma API key at runtime (kept in module memory). Do NOT write it to disk."""
    global GEMMA_API_KEY
    GEMMA_API_KEY = key


def set_gemma_url(url: str):
    """Set the Gemma URL at runtime."""
    global GEMMA_URL
    GEMMA_URL = url


def _call_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    if not OPENAI_API_KEY:
        return (
            "No OPENAI_API_KEY found in environment. To enable OpenAI responses, "
            "set the OPENAI_API_KEY environment variable."
        )

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.7,
    }
    resp = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return json.dumps(data)


def _call_gemma(prompt: str, gemma_url: Optional[str] = None, api_key: Optional[str] = None) -> str:
    url = gemma_url or GEMMA_URL
    key = api_key or GEMMA_API_KEY
    if not url:
        return (
            "No GEMMA_URL found in environment. To use Gemma, set the GEMMA_URL env var to the API endpoint."
        )
    if not key:
        return (
            "No GEMMA_API_KEY found in environment. To use Gemma, set the GEMMA_API_KEY env var to your key."
        )

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    payload = {"prompt": prompt}

    resp = requests.post(url, headers=headers, json=payload, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    for k in ("text", "response", "result", "output"):
        if isinstance(data, dict) and k in data:
            val = data[k]
            if isinstance(val, str):
                return val.strip()
            if isinstance(val, list) and val:
                return str(val[0]).strip()

    try:
        return data["choices"][0].get("text") or data["choices"][0].get("message", {}).get("content")
    except Exception:
        return json.dumps(data)


def get_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Return a text response for the given prompt using the selected provider."""
    if not prompt:
        return ""

    if AI_PROVIDER == "gemma":
        return _call_gemma(prompt)
    else:
        return _call_openai(prompt, model=model)


# ===========================================================
# 👇 ADD YOUR GEMMA SETTINGS BELOW (safe section)
# ===========================================================
if __name__ == "__main__":
    # Paste your Gemma API key and URL here (do NOT edit the functions above)
    set_gemma_api_key("AIzaSyAip6sQ25rGgEOYpJcGdehOAkOFO91mjUw")
    set_gemma_url("http://localhost:11434/api/generate")

    # Test it
    print(get_response("Hello, Gemma!"))
