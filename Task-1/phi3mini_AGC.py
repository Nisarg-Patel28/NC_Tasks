import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_article(prompt : str) -> str:
    "Send a prompt"
    params  = {
        "model":"phi3:mini",
        "prompt":prompt,
        "stream":False
    }
    response = requests.post(OLLAMA_URL, json=params)
    response.raise_for_status() 
    data = response.json()
    return data.get("response", "")