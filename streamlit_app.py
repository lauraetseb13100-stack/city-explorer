import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer", layout="wide")

st.title("📍 City Explorer")
st.subheader("Ton agrégateur d'événements locaux")

# --- CONNEXION ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Tu as raison, on reste sur le 2.5 si tu préfères sa puissance !
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except Exception as e:
    st.error("Problème de configuration.")
    st.stop()

# --- INTERFACE ---
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

# Utilisation du cache Streamlit pour ne pas re-demander à Google la même chose
@st.cache_data(ttl=3600) # Garde en mémoire pendant 1 heure
def chercher_evenements(ville, date, categories):
    prompt = f"""
    Nous sommes le 21 février 2026. Recherche les {categories} à {ville} le {date}.
    CONSIGNES :
    1. GRANDS TITRES (ex: VIDE-GRENIERS).
    2. Point par point : • [Nom] : [Lieu] - [Horaire] (Source : [Nom])
    3. SI RIEN : réponds 'RIEN'.
    4. AUCUNE intro.
    """
    response = model.generate_content(prompt)
    return response

if st.button("Lancer la recherche globale"):
    try:
        with st.spinner("Interrogation des bases de données..."):
            response = chercher_evenements(ville, date_choisie, categories)
            
            if not response.candidates:
                st.warning("Réponse bloquée par les filtres. Réessaie.")
            else:
                resultat = response.text.strip()
                st.markdown("---")
                if not resultat or "RIEN" in resultat.upper() and len(resultat) < 10:
                    st.info("Pas d'événement ce jour")
                else:
                    st.markdown(resultat)
                    
    except Exception as e:
        if "429" in str(e):
            st.error("Quota atteint (Modèle 2.5). Patiente 60 secondes avant de recliquer.")
        else:
            st.error(f"Détail technique : {e}")

# Bouton pour vider le cache si tu veux vraiment forcer une nouvelle recherche
if st.button("Effacer l'historique de recherche"):
    st.cache_data.clear()
    st.success("Mémoire vidée !")
