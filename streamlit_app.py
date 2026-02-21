import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer")
st.title("📍 City Explorer")

# Ta clé du 14 février
API_KEY = "AIzaSyA5PJn70aruuCJxgHWAIEbSiHvhW0rbVOY" 

genai.configure(api_key=API_KEY)

# CETTE LIGNE EST LA CLÉ : On utilise 'gemini-1.5-flash-latest' 
# C'est le nom qui ne renvoie jamais de 404
model = genai.GenerativeModel('gemini-1.5-flash-latest')

ville = st.text_input("Quelle ville ?", "Marseille")
date_choisie = st.date_input("Date")

if st.button("Lancer la recherche"):
    with st.spinner("Analyse des données..."):
        try:
            # On demande une réponse simple pour tester
            response = model.generate_content(f"Quoi faire à {ville} le {date_choisie} ?")
            st.success("Ça marche !")
            st.write(response.text)
        except Exception as e:
            st.error(f"Erreur technique : {e}")
