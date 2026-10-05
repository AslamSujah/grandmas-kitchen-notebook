from src.transcribe import transcribe_audio
from src.ocr import extract_text_from_image
from src.llm_parser import parse_recipe


def process_inputs(audio_path=None, image_path=None):
    chunks = []

    if audio_path:
        t = transcribe_audio(audio_path)
        if t:
            chunks.append("[AUDIO]\n" + t)

    if image_path:
        t = extract_text_from_image(image_path)
        if t:
            chunks.append("[IMAGE]\n" + t)

    raw = "\n\n".join(chunks).strip()
    if not raw:
        return {"title": "No content", "ingredients": [], "steps": [], "story": ""}

    return parse_recipe(raw)
