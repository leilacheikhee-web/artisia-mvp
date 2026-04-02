import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

def call_llm(prompt, model=OLLAMA_MODEL, format="json"):
    """
    Shared LLM client function.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "format": format,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None
