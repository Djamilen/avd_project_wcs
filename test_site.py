import streamlit as st
import pandas as pd

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("df_descriptif.csv")  # Remplace par ton fichier
    return df

df = load_data()

st.title("🎬 Recherche de Films")

# Barre de recherche
search_query = st.text_input("🔍 Titre du film :")

# Suggestion dynamique de titres
if search_query:
    titres_suggérés = df[df['originalTitle'].str.startswith(search_query, case=False, na=False)]['originalTitle'].unique().tolist()
    if titres_suggérés:
        st.markdown("**Suggestions :**")
        for titre in titres_suggérés[:10]:  # Limite à 10 suggestions
            st.write("🔹", titre)

# Filtres de genre
genres_disponibles = df['genres'].dropna().unique().tolist()
genres_selectionnes = st.multiselect("🎞️ Filtrer par genre :", genres_disponibles)

# Application des filtres
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['originalTitle'].str.contains(search_query, case=False, na=False)]

if genres_selectionnes:
    filtered_df = filtered_df[filtered_df['genres'].isin(genres_selectionnes)]

# Résultats
st.write(f"🎥 {len(filtered_df)} film(s) trouvé(s) :")
st.dataframe(filtered_df[['originalTitle', 'genres', 'startYear']])  # Adapte les colonnes à ton DataFrame
