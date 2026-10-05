# Grandma's Kitchen Notebook

An open-source AI app that converts family voice notes + handwritten recipe cards into structured recipes.

## Stack
- faster-whisper (open speech model)
- Tesseract OCR
- Gemma via Ollama
- Streamlit
- SQLite

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Render deploy
- Push this repo to GitHub
- Connect repo in Render
- Use Docker deploy
- Start command is inside Dockerfile