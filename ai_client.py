import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# WARNING: gemini-2.0-flash-exp is deprecated. 
# It might be safer to switch to "gemini-2.5-flash" if issues persist.
GEMINI_MODEL = "gemini-2.0-flash-exp" 

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

DEFAULT_TIMEOUT = 30


def get_response(prompt: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
    """
    Sends a prompt to the Gemini API and returns the response text.
    Includes robust error detection and logging.
    """
    if not GEMINI_API_KEY:
        print("API ERROR: GEMINI_API_KEY is not set. Check your .env file.")
        return None

    if not prompt.strip():
        return ""

    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status() # Raises an exception for 4xx/5xx status codes
        
        data = resp.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError, TypeError):
            print("Bad response format or content blocked. Full response data:")
            print(data)
            return ""

    except requests.exceptions.HTTPError as e:
        print(f"API HTTP ERROR: {e}")
        print(f"Status Code: {e.response.status_code}. Response Text: {e.response.text[:150]}...")
        if e.response.status_code == 400:
             print("HINT: A 400 error often means an invalid API key, model name, or malformed request.")
        return None
        
    except requests.exceptions.Timeout as e:
        print(f"API TIMEOUT ERROR: Request timed out after {timeout} seconds.")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"API CONNECTION/REQUEST ERROR: {type(e).__name__}: {e}")
        return None

    except Exception as e:
        print(f"API UNEXPECTED ERROR: {type(e).__name__}: {e}")
        return None