import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer")
st.title("📍 City Explorer")

# Remplace bien par ta clé AIza...
API_KEY = "AIzaSyABoY4UuLdz3La0vS4yHed6qJm3M7x5QDY" 

genai.configure(api_key=API_KEY)

# On teste avec le nom complet technique
model = genai.GenerativeModel('models/gemini-pro')

ville = st.text_input("Quelle ville ?", "Marseille")
date_choisie = st.date_input("Date")

if st.button("Lancer la recherche"):
    if "AIza" not in API_KEY:
        st.error("Ta clé API ne semble pas correcte.")
    else:
        with st.spinner("Recherche..."):
            try:
                # Utilisation d'un prompt très simple
                response = model.generate_content(f"Quoi faire à {ville} le {date_choisie} ?")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erreur : {e}")
