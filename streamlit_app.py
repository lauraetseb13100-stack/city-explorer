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
    st.error("Clé API non configurée.")
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
        
        prompt = f"""
        Nous sommes le 21 février 2026. 
        Recherche les {categories} à {ville} le {date_choisie}.
        
        CONSIGNES :
        1. Organise par GRANDS TITRES (ex: VIDE-GRENIERS).
        2. Liste à puces : • [Nom] : [Lieu] - [Horaire] (Source : [Nom])
        3. SI TU NE TROUVES RIEN, réponds exactement et uniquement par ce mot : RIEN
        4. AUCUNE phrase d'introduction ni de conclusion.
        """
        
        try:
            response = model.generate_content(prompt)
            resultat = response.text.strip()
            
            st.markdown("---")
            
            # Vérification si l'IA n'a rien trouvé
            if not resultat or "RIEN" in resultat.upper() and len(resultat) < 10:
                st.info("Pas d'événement ce jour")
            else:
                st.markdown(resultat)
                
        except Exception as e:
            # On garde l'erreur rouge uniquement si c'est une panne technique (ex: clé API)
            st.error(f"Un problème technique est survenu.")
