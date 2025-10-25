import os
import json
import requests
from typing import Optional

# ===========================================================
# CONFIG
# ===========================================================
AI_PROVIDER = os.environ.get("AI_PROVIDER", "ollama").lower()

# Ollama settings
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default local Ollama endpoint
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")  # Default model

# ===========================================================
# SETTERS
# ===========================================================
def set_model(model: str):
    """Set the Ollama model at runtime (e.g., 'llama3.2', 'mistral')."""
    global OLLAMA_MODEL
    OLLAMA_MODEL = model

def set_url(url: str):
    """Set the Ollama API URL at runtime (useful for non-standard ports)."""
    global OLLAMA_API_URL
    OLLAMA_API_URL = url

def set_api_key(key: str = None):
    """No-op for compatibility with PyQt app; Ollama doesn't need an API key."""
    pass  # Ollama runs locally, so no API key is required

# ===========================================================
# CALLERS
# ===========================================================
def _call_ollama(prompt: str, model: Optional[str] = None) -> str:
    """Make a request to the local Ollama API."""
    url = OLLAMA_API_URL
    model = model or OLLAMA_MODEL

    if not model:
        return "No model specified. Set OLLAMA_MODEL in environment or use set_model()."

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,  # Non-streaming for PyQt compatibility
        "options": {
            "temperature": 0.7,
            "max_tokens": 512,
        }
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        if "response" in data:
            return data["response"].strip()
        
        return "Unexpected response format from Ollama."
    except requests.exceptions.ConnectionError:
        return "Failed to connect to Ollama. Ensure 'ollama serve' is running."
    except requests.exceptions.HTTPError as e:
        return f"Ollama API error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Ollama request failed: {str(e)}. Ensure model '{model}' is pulled (run 'ollama pull {model}')."

# ===========================================================
# PUBLIC API
# ===========================================================
def get_response(prompt: str, model: Optional[str] = None) -> str:
    """Unified response function for Ollama, compatible with PyQt app."""
    if not prompt:
        return ""

    if AI_PROVIDER == "ollama":
        return _call_ollama(prompt, model=model)
    else:
        return "Only Ollama provider is supported in this version."

# ===========================================================
# BACKWARD COMPATIBILITY ALIAS
# ===========================================================
ai_gemma = get_response

# ===========================================================
# MANUAL TEST (Optional)
# ===========================================================
if __name__ == "__main__":
    print("🔍 Testing Ollama connection...")
    response = get_response("Hello Ollama, are you online?")
    print(response)