import streamlit as st
st.set_page_config(
    layout="wide",
    page_title="CINE PROJECT",
    page_icon="🎬",
    initial_sidebar_state="expanded"
)
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
import re
from page_n import accueil, session_states, recherche, espace_decouverte, reco


session_states()

# Lire le fichier CSV (placé dans le même dossier que ce script)
@st.cache_data 
def load_data():
    df = pd.read_csv("csv/df_final.csv")
    df = df[df['url_complet'].notna() & df['startYear'].astype(str).str.isdigit()]
    df['startYear'] = df['startYear'].astype(int)
    df = df.set_index(df['primaryTitle'] + "_" + df['startYear'].astype(str))
    return df.sort_values("startYear", ascending=False)

# Charger les données dans session_state 
if "csv/df_final" not in st.session_state:
    st.session_state["csv/df_final"] = load_data()

# Importer les pages SEULEMENT APRÈS le set_page_config

# Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche", "Espace découverte", "Reco"],
        icons=["film", "search", "stars"],
        menu_icon="camera-reels",
        default_index=["Accueil", "Recherche", "Espace découverte", "Reco"].index(st.session_state.page)
         )
    if selection != st.session_state.page:
        st.session_state.page = selection
if selection == "Accueil":
   accueil()

elif selection == "Recherche":
    recherche()

elif selection == "Espace découverte":
    espace_decouverte()

elif selection == "Reco":
    reco()