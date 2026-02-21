import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="City Explorer")
st.title("📍 City Explorer")

# Colle ta nouvelle clé ici
API_KEY = "AIzaSyBpOPKmsy71csnVyCKwMww0YrnicdoXXCo" 

genai.configure(api_key=API_KEY)

# Utilisation du nom le plus simple sans le préfixe 'models/'
# car Streamlit semble l'ajouter tout seul dans ta version
model = genai.GenerativeModel('gemini-1.5-flash')

ville = st.text_input("Quelle ville ?", "Marseille")
date_choisie = st.date_input("Date")

if st.button("Lancer la recherche"):
    if "AIza" not in API_KEY:
        st.error("Ta clé API n'est pas configurée.")
    else:
        with st.spinner("Recherche en cours..."):
            try:
                # On force une question très simple pour tester
                response = model.generate_content(f"Liste 3 sorties à {ville} le {date_choisie}")
                st.success("Connexion réussie !")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erreur persistante : {e}")
                st.info("Si l'erreur 404 persiste, c'est un délai d'activation chez Google (compte 24h).")
