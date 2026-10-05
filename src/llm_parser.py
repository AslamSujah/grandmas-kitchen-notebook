import json
import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")

PROMPT = """
You are a recipe extraction assistant.
Return STRICT JSON with:
title, ingredients (array), steps (array), story

Input:
{raw}
"""

def parse_recipe(raw_text: str) -> dict:
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": PROMPT.format(raw=raw_text), "stream": False},
            timeout=120
        )
        r.raise_for_status()
        out = r.json().get("response", "").strip()
        data = json.loads(out)
        data.setdefault("title", "Untitled Recipe")
        data.setdefault("ingredients", [])
        data.setdefault("steps", [])
        data.setdefault("story", "")
        return data
    except Exception:
        return {
            "title": "Untitled Recipe",
            "ingredients": [],
            "steps": [raw_text[:1200]],
            "story": "Fallback parse used"
        }