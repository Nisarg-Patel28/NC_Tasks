import json 
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_article(prompt):
    payload = {
        "model":"mistral:7b",
        "prompt":prompt,
        "stream":False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200: #This checks whether the status code is exactly 200 which means OK or Success.
        return response.json().get("response","")
    else:
        return f"Error! {response.status_code} - {response.text}" 