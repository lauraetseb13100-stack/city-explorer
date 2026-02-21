import streamlit as st
import google.generativeai as genai
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="City Explorer", layout="wide")
st.title("📍 City Explorer")

# --- TA CLÉ ICI ---
API_KEY = "AIzaSyABoY4UuLdz3La0vS4yHed6qJm3M7x5QDY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash', tools=['google_search_retrieval'])

ville = st.text_input("Quelle ville ?", "Marseille")
date_choisie = st.date_input("Pour quelle date ?")
categories = st.multiselect("Catégories", ["Vide-greniers", "Brocantes", "Marchés", "Recycleries"], default=["Vide-greniers"])

if st.button("Rechercher"):
    with st.spinner("L'IA cherche sur Google..."):
        prompt = f"Donne les {categories} à {ville} le {date_choisie}. Format: Nom | Adresse | Ville | Lat | Lon"
        response = model.generate_content(prompt)
        st.write(response.text)
        st.info("Bravo ! Ton app est connectée à l'IA.")
