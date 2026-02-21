import streamlit as st
import google.generativeai as genai

st.title("Diagnostic de connexion")

# Ta clé du 14 février
API_KEY = "AIzaSyA5PJn70aruuCJxgHWAIEbSiHvhW0rbVOY" 

try:
    genai.configure(api_key=API_KEY)
    
    # Étape 1 : Lister TOUS les modèles que ta clé peut voir
    models = genai.list_models()
    model_list = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
    
    if model_list:
        st.success(f"Connexion réussie ! Voici les modèles que tu peux utiliser :")
        st.write(model_list)
        
        # Étape 2 : Tester automatiquement le premier de la liste
        choix = model_list[0]
        st.info(f"Test automatique avec : {choix}")
        m = genai.GenerativeModel(choix)
        reponse = m.generate_content("Dis 'OK'")
        st.write("Résultat du test :", reponse.text)
    else:
        st.error("Ta clé est connectée mais aucun modèle n'est disponible.")

except Exception as e:
    st.error(f"L'erreur vient de là : {e}")
