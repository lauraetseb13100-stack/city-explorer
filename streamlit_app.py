import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer", layout="wide")

st.title("📍 City Explorer")
st.subheader("Trouvez les vide-greniers et brocantes avec l'IA")

API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)

# On utilise le modèle qui a répondu "OK" tout à l'heure
model = genai.GenerativeModel('models/gemini-2.5-flash')

col1, col2 = st.columns(2)
with col1:
    ville = st.text_input("Quelle ville ?", "Marseille")
with col2:
    date_choisie = st.date_input("Pour quelle date ?")

categories = st.multiselect(
    "Type d'événement",
    ["Vide-greniers", "Brocantes", "Marchés", "Recycleries"],
    default=["Vide-greniers", "Brocantes"]
)

if st.button("Lancer la recherche"):
    with st.spinner(f"Recherche en cours pour {ville}..."):
        # On force la date du jour pour que l'IA ne soit pas perdue
        aujourdhui = "21 février 2026"
        
        prompt = f"""
        CONSIGNE IMPORTANTE : Nous sommes aujourd'hui le {aujourdhui}. 
        C'est la date actuelle réelle.
        
        En tant qu'expert local, liste les {categories} prévus à {ville} le {date_choisie}.
        Pour chaque résultat :
        1. Donne le nom exact et l'adresse.
        2. Donne les horaires.
        3. Si tu n'as pas l'événement exact pour cette date précise, liste les marchés ou lieux de brocante permanents à {ville} qui sont ouverts le {date_choisie}.
        """
        
        try:
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            st.success("Recherche terminée !")
        except Exception as e:
            st.error(f"Erreur : {e}")
