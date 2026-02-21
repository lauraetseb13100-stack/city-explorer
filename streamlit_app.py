import streamlit as st
import google.generativeai as genai
from datetime import datetime

st.set_page_config(page_title="City Explorer Pro", layout="wide")

# Style personnalisé pour rendre l'app plus esthétique
st.markdown("""
    <style>
    .stTitle { color: #2E4053; font-family: 'Helvetica'; }
    .day-header { color: #1B4F72; font-weight: bold; font-size: 22px; margin-top: 20px; border-bottom: 2px solid #AED6F1; }
    .cat-header { color: #A04000; font-weight: bold; text-transform: uppercase; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📍 City Explorer Pro")
st.subheader("Planification de sorties et brocantes")

# --- CONNEXION ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    st.error("Clé API non trouvée dans les Secrets.")
    st.stop()

# --- BARRE LATÉRALE DE CONFIGURATION ---
with st.sidebar:
    st.header("Paramètres")
    # Liste défilante des villes principales (on peut l'enrichir)
    ville = st.selectbox("Choisir une ville", 
                         ["Marseille", "Aix-en-Provence", "Sarlat-la-Canéda", "Nice", "Lyon", "Bordeaux", "Avignon", "Arles"])
    
    # Rayon de recherche
    rayon = st.slider("Rayon autour de la ville (km)", 0, 50, 20)
    
    # Plage de dates
    st.write("Période de recherche :")
    dates = st.date_input("Sélectionner les dates", 
                         value=(datetime(2026, 2, 21), datetime(2026, 2, 28)),
                         min_value=datetime(2026, 2, 21))

# --- INTERFACE PRINCIPALE ---
categories = st.pills("Types d'événements", 
                     ["Vide-greniers", "Brocantes", "Marchés", "Fêtes de village"], 
                     selection_mode="multi",
                     default=["Vide-greniers", "Brocantes"])

if st.button("Lancer la recherche pour la période"):
    if len(dates) < 2:
        st.warning("Veuillez sélectionner une date de début et une date de fin sur le calendrier.")
    else:
        date_debut, date_fin = dates
        with st.spinner(f"Analyse du secteur ({rayon}km autour de {ville})..."):
            
            prompt = f"""
            Aujourd'hui nous sommes le 21 février 2026.
            Tu es un assistant de voyage. Liste les {categories} dans un rayon de {rayon}km autour de {ville}.
            Période : du {date_debut} au {date_fin}.
            
            FORMAT DE RÉPONSE STRICT (Respecte les balises Markdown pour le style) :
            
            ## Le [Jour de la semaine] [Date]
            ### [CATÉGORIE EN MAJUSCULES]
            - **[NOM DE L'ÉVÉNEMENT]** : [Commune exacte], [Adresse] - [Horaire]
            
            CONSIGNES :
            - Regroupe par jour.
            - Si rien pour un jour, ne l'affiche pas.
            - Ne fais aucune phrase d'introduction.
            - Utilise les données de Vide-greniers.org, Jours-de-marché et les sites de mairies.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown(f"## 🗓️ Résultats pour {ville} (+{rayon}km)")
                st.markdown(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.error("Le quota est atteint. Attends 60 secondes. La recherche sur une semaine est gourmande !")
                else:
                    st.error(f"Erreur : {e}")

if st.button("Effacer le cache"):
    st.cache_data.clear()
    st.rerun()
