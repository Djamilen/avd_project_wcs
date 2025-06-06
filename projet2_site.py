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
    return pd.read_csv("df_descriptif.csv")

# Charger les données dans session_state 
if "df_descriptif" not in st.session_state:
    st.session_state["df_descriptif"] = load_data()

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
