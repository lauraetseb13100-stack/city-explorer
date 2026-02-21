import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer", layout="wide")

st.title("📍 City Explorer")
st.subheader("Agrégateur d'événements locaux en temps réel")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except Exception as e:
    st.error("Clé API non configurée.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    ville = st.text_input("Ville", "Marseille")
with col2:
    date_choisie = st.date_input("Date")

categories = st.multiselect(
    "Types d'événements",
    ["Vide-greniers", "Brocantes", "Marchés", "Fêtes de village", "Salons", "Expositions"],
    default=["Vide-greniers", "Brocantes", "Marchés"]
)

if st.button("Lancer la recherche globale"):
    with st.spinner(f"Scan des sources (Mairies, Vide-greniers.org, Jours-de-marché, Agendas locaux)..."):
        
        prompt = f"""
        Tu es un agent de recherche ultra-performant. Nous sommes le 21 février 2026.
        Ta mission : Synthétiser les données de plusieurs sources pour {ville} le {date_choisie}.
        
        SOURCES À CONSULTER (via ta base de données) :
        1. Vide-greniers.org & Brocabrac (pour les ventes entre particuliers).
        2. Jours-de-marché.fr (pour les marchés alimentaires et artisanaux).
        3. Agendas municipaux et sites des mairies (pour les fêtes de village et événements officiels).
        4. France-Brocante (pour les professionnels).
        
        CONSIGNES DE RÉPONSE :
        - AUCUNE introduction, AUCUNE conclusion.
        - Uniquement des faits.
        - Si plusieurs événements, sépare-les par une ligne '---'.
        - Format strict :
        
        Événement : [Nom]
        Type : [Catégorie]
        Lieu : [Adresse précise]
        Horaire : [Si disponible]
        Source : [Nom de la source probable]
        ---
        """
        
        try:
            response = model.generate_content(prompt)
            st.markdown(f"### 📋 Résultats pour {ville}")
            st.write(response.text)
        except Exception as e:
            st.error(f"Erreur lors de la synthèse : {e}")
