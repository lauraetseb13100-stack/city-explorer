import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer", layout="wide")
st.title("📍 City Explorer")

API_KEY = "AIzaSyABoY4UuLdz3La0vS4yHed6qJm3M7x5QDY" 

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')

ville = st.text_input("Quelle ville ?", "Marseille")
date_choisie = st.date_input("Pour quelle date ?")

if st.button("Lancer la recherche"):
    if API_KEY == "TON_API_KEY_ICI":
        st.error("N'oublie pas de coller ta clé API dans le code !")
    else:
        with st.spinner(f"Recherche en cours pour {ville}..."):
            prompt = f"Liste les vide-greniers et marchés à {ville} le {date_choisie}."
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🔍 Résultats")
                st.write(response.text)
            except Exception as e:
                st.error(f"Détail de l'erreur : {e}")
