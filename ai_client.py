"""
Simple AI client wrapper with flexible provider selection.

Supports:
 - openai (requires OPENAI_API_KEY)
 - gemma (requires GEMMA_URL and GEMMA_API_KEY)
"""

import os
import json
import requests
from typing import Optional

# ===========================================================
# CONFIG
# ===========================================================
AI_PROVIDER = os.environ.get("AI_PROVIDER", "gemma").lower()

# OpenAI settings
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Gemma settings
GEMMA_URL = os.environ.get("GEMMA_URL")
GEMMA_API_KEY = os.environ.get("GEMMA_API_KEY")


# ===========================================================
# SETTERS
# ===========================================================
def set_api_key(key: str):
    """Set the Gemma API key at runtime (kept in memory only)."""
    global GEMMA_API_KEY
    GEMMA_API_KEY = key


def set_url(url: str):
    """Set the Gemma URL at runtime."""
    global GEMMA_URL
    GEMMA_URL = url


# ===========================================================
# CALLERS
# ===========================================================
def _call_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    if not OPENAI_API_KEY:
        return "⚠️ No OPENAI_API_KEY found. Set it as an environment variable."

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

    try:
        resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ OpenAI request failed: {e}"


def _call_gemma(prompt: str, gemma_url: Optional[str] = None, api_key: Optional[str] = None) -> str:
    url = gemma_url or GEMMA_URL
    key = api_key or GEMMA_API_KEY
    if not url:
        return "⚠️ No GEMMA_URL found. Set GEMMA_URL in environment or in code."
    if not key:
        return "⚠️ No GEMMA_API_KEY found. Set GEMMA_API_KEY in environment or in code."

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    payload = {"model": "gemma", "prompt": prompt}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        # Try various response formats
        for k in ("text", "response", "result", "output"):
            if isinstance(data, dict) and k in data:
                val = data[k]
                if isinstance(val, str):
                    return val.strip()
                if isinstance(val, list) and val:
                    return str(val[0]).strip()

        if "choices" in data and data["choices"]:
            c = data["choices"][0]
            return c.get("text") or c.get("message", {}).get("content", "")

        return str(data)
    except Exception as e:
        return f"❌ Gemma request failed: {e}"


# ===========================================================
# PUBLIC API
# ===========================================================
def get_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Unified response function"""
    if not prompt:
        return ""

    if AI_PROVIDER == "gemma":
        return _call_gemma(prompt)
    return _call_openai(prompt, model=model)


# ===========================================================
# BACKWARD COMPATIBILITY ALIAS
# ===========================================================
# So dashboard.py can still use `ai_gemma(prompt)`
ai_gemma = get_response


# ===========================================================
# MANUAL TEST (Optional)
# ===========================================================
if __name__ == "__main__":
    # Insert your local Gemma settings here:
    set_url("http://localhost:11434/api/generate")

    print("🔍 Testing Gemma connection...")
    print(ai_gemma("Hello Gemma, are you online?"))
