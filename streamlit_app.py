import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer", layout="wide")

st.title("📍 City Explorer")
st.subheader("Trouvez les vide-greniers et brocantes avec l'IA")

# Ta clé API qui fonctionne
API_KEY = "AIzaSyA5PJn70aruuCJxgHWAIEbSiHvhW0rbVOY" 

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
        # On demande à l'IA d'utiliser ses connaissances de 2026
        prompt = f"Liste les {categories} à {ville} le {date_choisie}. Donne les adresses et horaires si possible."
        
        try:
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            st.success("Recherche terminée !")
        except Exception as e:
            st.error(f"Erreur : {e}")
        st.error("Ta clé est connectée mais aucun modèle n'est disponible.")

except Exception as e:
    st.error(f"L'erreur vient de là : {e}")
