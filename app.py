import streamlit as st
from pathlib import Path
from src.db import init_db, insert_recipe, list_recipes
from src.pipeline import process_inputs

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="Grandma's Kitchen Notebook", layout="wide")
st.title("🍲 Grandma's Kitchen Notebook")
st.caption("Open-source AI recipe memory tool (audio + handwritten cards)")

init_db()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Family Memory")
    audio_file = st.file_uploader("Voice memo (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])
    image_file = st.file_uploader("Recipe image (png/jpg/jpeg)", type=["png", "jpg", "jpeg"])

    if st.button("Process"):
        audio_path = None
        image_path = None

        if audio_file:
            audio_path = str(UPLOAD_DIR / audio_file.name)
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())

        if image_file:
            image_path = str(UPLOAD_DIR / image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.read())

        with st.spinner("Running AI pipeline..."):
            recipe = process_inputs(audio_path, image_path)

        st.success("Done")
        st.json(recipe)

        ingredients_text = "\n".join([f"- {x}" for x in recipe.get("ingredients", [])])
        steps_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(recipe.get("steps", []))])

        insert_recipe(
            title=recipe.get("title", "Untitled Recipe"),
            ingredients=ingredients_text,
            steps=steps_text,
            story=recipe.get("story", ""),
            source_audio=audio_path,
            source_image=image_path
        )
        st.success("Saved to local DB")

with col2:
    st.subheader("Saved Recipes")
    recipes = list_recipes()
    if not recipes:
        st.info("No recipes yet.")
    else:
        for r in recipes:
            with st.expander(f"#{r['id']} - {r['title']}"):
                st.markdown("**Ingredients**")
                st.text(r["ingredients"] or "")
                st.markdown("**Steps**")
                st.text(r["steps"] or "")
                st.markdown("**Story**")
                st.write(r["story"] or "")