import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta

st.set_page_config(page_title="City Explorer Pro", layout="wide")

# --- CONNEXION ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    st.error("Clé API absente.")
    st.stop()

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("📍 Destination")
    ville = st.text_input("Ville/Village :", "Sarlat-la-Canéda")
    rayon = st.slider("Rayon (km)", 0, 50, 20)
    
    st.header("📅 Ta Semaine")
    date_debut = st.date_input("Début", datetime(2026, 2, 26))
    date_fin = st.date_input("Fin", datetime(2026, 3, 5))

# --- INTERFACE ---
categories = st.pills("Type", ["Vide-greniers", "Brocantes", "Marchés", "Fêtes"], 
                     selection_mode="multi", default=["Vide-greniers", "Brocantes"])

if st.button("🚀 GÉNÉRER MON PROGRAMME COMPLET", type="primary"):
    # On calcule le nombre de jours
    delta = date_fin - date_debut
    
    st.markdown(f"# 🗓️ Agenda du {date_debut} au {date_fin}")
    st.info(f"Recherche autour de {ville} (+{rayon}km)...")

    # LA BOUCLE : On interroge l'IA jour après jour automatiquement
    for i in range(delta.days + 1):
        jour_actuel = date_debut + timedelta(days=i)
        nom_jour = jour_actuel.strftime('%A %d %B')
        
        with st.expander(f"🔍 Analyse du {nom_jour}...", expanded=True):
            prompt = f"""
            Date : {jour_actuel}. 
            Cherche les {categories} à {ville} ({rayon}km).
            Format : • [NOM] : [LIEU] - [HORAIRE] (Source)
            Si rien, réponds 'AUCUN'. Pas d'intro.
            """
            
            try:
                response = model.generate_content(prompt)
                res = response.text.strip()
                if "AUCUN" in res.upper() and len(res) < 10:
                    st.write("Pas d'événements trouvés.")
                else:
                    st.markdown(f"**{nom_jour.upper()}**")
                    st.markdown(res)
            except Exception as e:
                st.warning(f"Pause quota sur ce jour... (Attente auto)")
                # On ne bloque pas tout, on continue au jour suivant

if st.button("Effacer le cache"):
    st.cache_data.clear()
    st.rerun()
