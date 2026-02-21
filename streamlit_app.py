import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer", layout="wide")

st.title("📍 City Explorer")
st.subheader("Trouvez vos sorties en un clic")

API_KEY = "AIzaSyABoY4UuLdz3La0vS4yHed6qJm3M7x5QDY"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

col1, col2 = st.columns(2)
with col1:
    ville = st.text_input("Quelle ville ?", "Marseille")
with col2:
    date_choisie = st.date_input("Pour quelle date ?")

categories = st.multiselect(
    "Que cherchez-vous ?",
    ["Vide-greniers", "Brocantes", "Marchés locaux", "Recycleries", "Escape Games"],
    default=["Vide-greniers"]
)

if st.button("Lancer la recherche"):
    with st.spinner(f"Recherche en cours pour {ville}..."):
        prompt = f"""
        En tant qu'expert local, liste les événements et lieux suivants : {categories} 
        à {ville} pour la date du {date_choisie}.
        Donne pour chaque résultat : le nom, l'adresse précise et une courte description.
        Si tu ne trouves pas d'événement spécifique à cette date, propose les lieux permanents 
        (comme les recycleries ou les marchés hebdomadaires).
        """
        
        try:
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
