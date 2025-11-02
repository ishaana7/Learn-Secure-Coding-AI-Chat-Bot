import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

resp = requests.get(URL, timeout=10)
if resp.status_code != 200:
    print(f"HTTP {resp.status_code}: {resp.text}")
else:
    data = resp.json()
    print("Available models:")
    for model in data.get("models", []):
        print(f" - {model['name']} ({model.get('displayName','')})")
