import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
import re

st.set_page_config(
    layout="wide",
    page_title="CINE PROJECT",
    page_icon="🎬",
    initial_sidebar_state="expanded"
)

# Lire le fichier CSV (placé dans le même dossier que ce script)
@st.cache_data 
def load_data():
    return pd.read_csv("df_sans_vec.csv")

# Charger les données dans session_state 
if "df_sans_vec" not in st.session_state:
    st.session_state["df_sans_vec"] = load_data()

# Importer les pages SEULEMENT APRÈS le set_page_config
from pages import accueil, recherche, espace_découverte

# Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche", "Espace découverte"],
        icons=["film", "search", "stars"],
        menu_icon="camera-reels",
        default_index=0
         )
if selection == "Accueil":
   accueil()

elif selection == "Recherche":
    recherche()

elif selection == "Espace découverte":
    espace_découverte()

    # st.header(" 🎬 CINE PROJECT")
    # # Initialisation de la page interne "Besoin d'idées"
    # if "idee_page" not in st.session_state:
    #     st.session_state.idee_page = "themes"

    # # Affichage des boutons de thématiques
    # if st.session_state.idee_page == "themes":
    #     st.header("🌟 Besoin d'idées ?")
    #     st.write("""
    #         Découvrez nos suggestions et recommandations pour enrichir votre expérience cinématographique.  
    #         Nous mettons à jour nos idées régulièrement, restez connectés !
    #     """)
    #     st.subheader("Choisissez une thématique :")

    #     col1, col2 = st.columns(2)

    #     with col1:
    #         if st.button("Top films populaires".upper()):
    #             st.session_state.idee_page = "populaires"
    #         if st.button("Top meilleures critiques".upper()):
    #             st.session_state.idee_page = "critiques"
    #         if st.button("Top célébrités".upper()):
    #             st.session_state.idee_page = "célébrités"

    #     with col2:
    #         if st.button("À l'affiche".upper()):
    #             st.session_state.idee_page = "affiche"
    #         if st.button("Films cultes".upper()):
    #             st.session_state.idee_page = "cultes"
    #         if st.button("Les sagas".upper()):
    #             st.session_state.idee_page = "sagas"

    # # Affichage des recommandations selon le thème sélectionné
    # else:
    #     theme = st.session_state.idee_page
    #     st.header(f"🎬 Thématique : {theme.capitalize()}")
    #     recherche = st.text_input("🔍 Rechercher un film", placeholder="Tapez un titre ou un genre...")

    #     st.subheader("⭐ Suggestions de films :")

    #     theme_images = {
    #         "populaires": ["avatar.png", "wish.png"],
    #         "critiques": ["encanto.png"],
    #         "célébrités": ["vaiana.png"],
    #         "affiche": ["raya.png"],
    #         "cultes": ["lilostich.png"],
    #         "sagas": ["avatar.png", "vaiana.png"]
    #     }

    #     for img in theme_images.get(theme, []):
    #         st.image(img, caption=img.replace(".png", "").capitalize())

    #     if recherche:
    #         st.info(f"Vous avez recherché : **{recherche}**")

    #     if st.button("⬅ Retour"):
    #         st.session_state.idee_page = "themes"
