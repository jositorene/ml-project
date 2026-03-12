import streamlit as st
from PIL import Image
import json
from recomendaciones_json import cargar_recomendaciones
import subprocess
import re
import test_model
from test_model import analizar_frigorifico, obtener_ingredientes_ingles
import streamlit.components.v1 as components

def load_css():
    with open("styles/cards.css") as f:
        return f.read()
css = load_css()

# Configuration of the page
st.set_page_config(
    page_title="The Fridge Survival",
    page_icon="🥗",
 
   layout="wide"
)
#---------------------------------------------------------------------------------------------------------------------
#------------------------------TITLE AND DESCRIPTION--------------------------------
st.markdown("""
<style>
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.fancy-title {
    font-weight: 700;
    color: #000; /* puedes usar var(--text-primary) si defines la variable */
    line-height: 1.07;
    letter-spacing: -0.025em;
    margin-bottom: 1.25rem;
}
.fancy-title span {
    display: inline-block;
    animation: float 3s ease-in-out infinite;
}
</style>

<h1 class="fancy-title" style='text-align: center; color: #2b6cb0; font-size: 5rem'>
<span>📸</span> The fridge Survival. <span>🥗</span>
</h1>
<h4 style="color:#2b6cb0; font-family:'Segoe UI', sans-serif; font-weight:650; font-size: 2.5rem; text-align:center">Upload a picture of your refrigerator and we'll suggest recipes.</h4>
<br><br><br>
""", unsafe_allow_html=True)

# -------------------------------COLUMN LAYOUT--------------------------------
col1, col2 = st.columns(2)  # Creamos dos columnas

with col1:
    # -------------------------------Subir imagen(columna 1)--------------------------------
    uploaded_file = st.file_uploader("Upload an image to get started", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        #centrar imagen
        c1, c2, c3 = st.columns([1, 7, 1])
        with c2:
            st.image(img, caption="Uploaded Image", width=600)

with col2:
    #cargar y mostrar los ingredientes detectados
    if 'img' in locals():
        with st.spinner("Detecting ingredients..."):
            resultado = analizar_frigorifico(img)
            # Verificamos si detecto ingredientes
            if resultado and obtener_ingredientes_ingles(resultado):
                st.success("Ingredients detected successfully!")          
                # Mostrar ingredientes
                st.markdown("""<h3 style="color:#2b6cb0; font-family:'Segoe UI', sans-serif; font-weight:700;">🥕 Ingredients Found:</h3>""", unsafe_allow_html=True)
                ingredientes_ingles = obtener_ingredientes_ingles(resultado)     
                response_json = {
                    "ingredients": ingredientes_ingles
                }
                print("ingredientes_ingles")    

                # Save ingredientes_ingles directly as a JSON array
                with open("ingredients.json", "w", encoding="utf-8") as f:
                    json.dump(ingredientes_ingles, f, indent=4, ensure_ascii=False)

                print("JSON array saved to 'ingredients.json'")                           
                #Dando estilo
                html_badges = ""
                for ing in ingredientes_ingles:
                    html_badges += f'<span style="display:inline-block; background-color:#d4edda; color:#000; padding:6px 12px; margin:6px; border-radius:7px; font-weight:bold;">{ing}</span>'         
                st.markdown(html_badges, unsafe_allow_html=True)
                st.write("---")   


            else:
                st.error("No se encontro ningun ingrediente. Por favor, intenta con otra imagen.")

# -------------------------------- RECOMENDACIONES -------------------------------------
subprocess.run(["python3", "03_vectorize.py"])
subprocess.run(["python3", "04_FAISS.py"])

if 'ingredientes_ingles' in locals() and ingredientes_ingles:
    st.markdown("""<h3 style="color:#2b6cb0; font-family:'Segoe UI', sans-serif; font-weight:700; text-align:center">🍽️ Recommended recipes</h3>""", unsafe_allow_html=True)
    
    recipes = cargar_recomendaciones("recipe_suggestions.json")

    if recipes:
        cards_html = ""
        for receta in recipes:
            title = receta['title']
            directions = json.loads(receta["directions"])
            score = receta['similarity_score']
            link = receta["link"]
            if not link.startswith(("http://", "https://")):
                link = "https://" + link

            # Primeros 3 pasos + resto expandible
            preview = directions[:3]
            extra = directions[3:]

            steps = "".join([f"<div class='step'><span class='num'>{i+1}</span>{step}</div>" for i, step in enumerate(preview)])
            
            if extra:
                extra_steps = "".join([f"<div class='step'><span class='num'>{i+4}</span>{step}</div>" for i, step in enumerate(extra)])
                steps += f"""
                <details>
                    <summary>Show {len(extra)} more steps ▼</summary>
                    {extra_steps}
                </details>
                """

            cards_html += f"""
            <div class="card">
                <div class="card-header">
                    <div class="title">🍲 {title}</div>
                    <div class="score">★ {score:.2f} match</div>
                </div>
                <div class="steps-container">
                    {steps}
                </div>
                <div class="card-footer">
                    <a href="{link}" target="_blank">→ Ver receta completa</a>
                </div>
            </div>
            """

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            {css}
        </style>
        </head>
        <body>
            <div class="grid">
                {cards_html}
            </div>
        </body>
        </html>
        """
        # Calcular altura dinámica según número de recetas
        num_rows = (len(recipes) + 2) // 3
        height = num_rows * 380 + 40

        components.html(full_html, height=height, scrolling=False)
    else:
        st.info("No hay recetas recomendadas para los ingredientes detectados.")



        


