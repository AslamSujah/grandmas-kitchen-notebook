import sqlite3
from pathlib import Path

DB_PATH = Path("db/recipes.db")

def conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            ingredients TEXT,
            steps TEXT,
            story TEXT,
            source_audio TEXT,
            source_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        c.commit()

def insert_recipe(title, ingredients, steps, story="", source_audio=None, source_image=None):
    with conn() as c:
        c.execute("""
        INSERT INTO recipes (title, ingredients, steps, story, source_audio, source_image)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, ingredients, steps, story, source_audio, source_image))
        c.commit()

def list_recipes():
    with conn() as c:
        rows = c.execute("SELECT * FROM recipes ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]