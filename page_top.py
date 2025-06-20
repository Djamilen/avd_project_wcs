import streamlit as st
import pandas as pd

# Chargement du DataFrame
df = pd.read_csv("csv/df_descriptif.csv")

# Nettoyage des genres
df["genres"] = df["genres"].fillna("")
df["genres"] = df["genres"].str.replace("{", "", regex=False)\
                           .str.replace("}", "", regex=False)\
                           .str.replace("'", "", regex=False)\
                           .str.split(",")

# Extraire tous les genres uniques
df_exploded = df.explode("genres")
df_exploded["genre_unique"] = df_exploded["genres"].str.strip()
all_genres = sorted(df_exploded["genre_unique"].dropna().unique())

# Définir les genres principaux
main_genres = [
    "Comedy", "Drama", "Action", "Adventure", "Animation",
    "Thriller", "Sci-Fi", "Fantasy", "Romance", "Horror"
]
other_genres = sorted(set(all_genres) - set(main_genres))

# Affichage des genres principaux sur 2 lignes × 5 colonnes
st.header("Genres principaux")
selected_genres = []

rows = [main_genres[:5], main_genres[5:]]  # 2 lignes

for row in rows:
    cols = st.columns(5)
    for col, genre in zip(cols, row):
        if col.checkbox(genre, key=f"main_{genre}"):
            selected_genres.append(genre)

# Genres secondaires dans un expander
with st.expander("Afficher plus de genres"):
    cols = st.columns(3)
    for i, genre in enumerate(other_genres):
        if cols[i % 3].checkbox(genre, key=f"other_{genre}"):
            selected_genres.append(genre)

# Filtrage des films
if selected_genres:
    df_filtered = df[df["genres"].apply(lambda genres: all(g in genres for g in selected_genres))]

    # Top 5 trié par note
    top5 = df_filtered.sort_values(by="averageRating", ascending=False).head(5).reset_index(drop=True)

    if not top5.empty:
        st.subheader(f"Top 5 films pour genres sélectionnés")
        cols = st.columns(5)
        for i, (_, row) in enumerate(top5.iterrows()):
            with cols[i % 5]:
                st.image(row["url_complet"], caption=f"{row['primaryTitle']} ({row['averageRating']})", width=150)
    else:
        st.warning("Aucun film ne correspond exactement aux genres sélectionnés.")
else:
    st.info("Coche un ou plusieurs genres à gauche pour afficher les films.")
