import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer", layout="wide")

st.title("📍 City Explorer")
st.subheader("Ton agrégateur d'événements locaux")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except Exception as e:
    st.error("Clé API non configurée dans les Secrets.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    ville = st.text_input("Ville", "Marseille")
with col2:
    date_choisie = st.date_input("Date")

categories = st.multiselect(
    "Types d'événements",
    ["Vide-greniers", "Brocantes", "Marchés", "Fêtes de village"],
    default=["Vide-greniers", "Brocantes", "Marchés"]
)

if st.button("Lancer la recherche globale"):
    with st.spinner(f"Scan des sources en cours..."):
        
        # PROMPT AVEC MISE EN PAGE STRUCTURÉE
        prompt = f"""
        Aujourd'hui nous sommes le 21 février 2026. 
        Recherche les {categories} à {ville} le {date_choisie}.
        
        CONSIGNES DE MISE EN PAGE :
        1. Organise la réponse par GRANDS TITRES en majuscules pour chaque catégorie (ex: VIDE-GRENIERS, MARCHÉS).
        2. Sous chaque titre, utilise une liste à puces (un point par événement).
        3. Pour chaque point, respecte strictement ce format : 
           • [Nom de l'événement] : [Adresse/Lieu] - [Horaire] (Source : [Nom])
        4. Si une catégorie est vide, n'affiche pas le titre.
        5. AUCUNE phrase d'introduction ni de conclusion. Direct au but.
        """
        
        try:
            response = model.generate_content(prompt)
            st.markdown("---")
            # Utilisation de st.markdown pour que les titres et les puces s'affichent bien
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Erreur d'affichage : {e}")
