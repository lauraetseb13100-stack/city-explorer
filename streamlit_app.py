import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="City Explorer Gratuit", layout="wide")

# --- CONNEXION ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # On reste sur le Flash qui est GRATUIT et rapide
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# --- INTERFACE ---
with st.sidebar:
    st.title("📍 Configuration")
    ville = st.text_input("Ville centre :", "Sarlat-la-Canéda")
    rayon = st.slider("Rayon (km) :", 5, 50, 20)
    st.divider()
    date_debut = st.date_input("Du :", datetime(2026, 2, 26))
    date_fin = st.date_input("Au :", datetime(2026, 3, 5))

categories = st.pills("Activités", ["Vide-greniers", "Marchés", "Fêtes"], 
                     selection_mode="multi", default=["Vide-greniers", "Marchés"])

if st.button("📅 GÉNÉRER MON PROGRAMME (GRATUIT)", type="primary"):
    nb_jours = (date_fin - date_debut).days + 1
    
    if nb_jours > 10:
        st.warning("⚠️ Pour rester gratuit, limite-toi à 10 jours maximum.")
    else:
        progress_bar = st.progress(0)
        
        for i in range(nb_jours):
            jour_actuel = date_debut + timedelta(days=i)
            # Mise à jour de la barre de progression
            progress_bar.progress((i + 1) / nb_jours)
            
            st.markdown(f"### 🗓️ {jour_actuel.strftime('%A %d %B')}")
            
            # Le secret : un prompt ultra-court
            prompt = f"Date:{jour_actuel}. Liste {categories} à {ville} (+{rayon}km). Format: • Nom : Lieu - Horaire. Si rien: 'Aucun'."
            
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
                # LA PAUSE MAGIQUE : on attend 4 secondes pour que Google nous laisse tranquille
                time.sleep(4) 
                
            except Exception as e:
                if "429" in str(e):
                    st.warning("⏳ Google sature un peu... On attend 10 secondes et on continue.")
                    time.sleep(10)
                    # On réessaie une fois le même jour
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                else:
                    st.error(f"Erreur sur ce jour : {e}")

st.divider()
st.caption("Astuce : Si ça bloque, attends 1 minute sans cliquer et recommence.")
