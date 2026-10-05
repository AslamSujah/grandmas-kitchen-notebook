# Grandma's Kitchen Notebook

An open-source AI app that converts family voice notes + handwritten recipe cards into structured recipes.

## Features
- Audio transcription with faster-whisper
- OCR from recipe images with Tesseract
- Recipe parsing with Gemma/Ollama when configured
- Automatic fallback parser for cloud deployments without Ollama
- Local SQLite storage

## Deploy (Easiest)
Use Streamlit Community Cloud:
1. Push this repo to GitHub
2. Go to https://share.streamlit.io
3. Select this repo, branch `main`, file `app.py`
4. Deploy

## Optional LLM Configuration
Set these secrets/env vars to enable Ollama parsing:
- `OLLAMA_URL` (example: `http://your-ollama-host:11434/api/generate`)
- `OLLAMA_MODEL` (example: `gemma2:2b`)

Without these, the app still works in fallback mode.

## Local run
```bash
pip install -r requirements.txt
streamlit run app.py
```
