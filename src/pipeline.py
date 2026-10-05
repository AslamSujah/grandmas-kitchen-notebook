from src.transcribe import transcribe_audio
from src.ocr import extract_text_from_image
from src.llm_parser import parse_recipe


def process_inputs(audio_path=None, image_path=None):
    chunks = []
    errors = []

    if audio_path:
        try:
            t = transcribe_audio(audio_path)
            if t:
                chunks.append("[AUDIO]\n" + t)
        except Exception as e:
            errors.append(f"Audio transcription failed: {e}")

    if image_path:
        try:
            t = extract_text_from_image(image_path)
            if t:
                chunks.append("[IMAGE]\n" + t)
        except Exception as e:
            errors.append(f"Image OCR failed: {e}")

    raw = "\n\n".join(chunks).strip()
    if not raw:
        return {
            "title": "No content",
            "ingredients": [],
            "steps": errors,
            "story": "",
        }

    recipe = parse_recipe(raw)
    if errors:
        recipe["story"] = (recipe.get("story", "") + " " + " ".join(errors)).strip()
    return recipe
