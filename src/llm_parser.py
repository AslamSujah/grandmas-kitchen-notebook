import json
import os
import re
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "")
MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")

PROMPT = """
You are a recipe extraction assistant.
Return STRICT JSON with:
- title (string)
- ingredients (array of strings)
- steps (array of strings)
- story (string)

Input:
{raw}
"""


def _fallback_parse(raw_text: str) -> dict:
    lines = [ln.strip(" -•\t") for ln in raw_text.splitlines() if ln.strip()]
    title = "Untitled Family Recipe"
    ingredients = []
    steps = []

    for line in lines:
        lower = line.lower()
        if any(k in lower for k in ["cup", "tsp", "tbsp", "grams", "kg", "ml", "oil", "salt", "sugar", "flour", "rice", "egg"]):
            ingredients.append(line)
        else:
            steps.append(line)

    if lines:
        title = lines[0][:80]

    return {
        "title": title,
        "ingredients": ingredients[:30],
        "steps": steps[:30] if steps else ["Review the extracted text and refine manually."],
        "story": "Automatically parsed in fallback mode (no online LLM endpoint configured).",
    }


def _extract_json(text: str):
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def parse_recipe(raw_text: str) -> dict:
    if not OLLAMA_URL:
        return _fallback_parse(raw_text)

    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": PROMPT.format(raw=raw_text), "stream": False},
            timeout=90,
        )
        r.raise_for_status()
        out = r.json().get("response", "").strip()
        out_json = _extract_json(out)
        if not out_json:
            return _fallback_parse(raw_text)

        data = json.loads(out_json)
        data.setdefault("title", "Untitled Recipe")
        data.setdefault("ingredients", [])
        data.setdefault("steps", [])
        data.setdefault("story", "")

        if not isinstance(data["ingredients"], list):
            data["ingredients"] = [str(data["ingredients"])]
        if not isinstance(data["steps"], list):
            data["steps"] = [str(data["steps"])]

        return data
    except Exception:
        return _fallback_parse(raw_text)
