#
# Colonnes disponibles :

# [
# 0:"originalTitle"
# 1:"imdb_id"
# 2:"primaryTitle"
# 3:"averageRating"
# 4:"numVotes"
# 5:"titleType"
# 6:"startYear"
# 7:"runtimeMinutes"
# 8:"primaryName"
# 9:"primaryProfession"
# 10:"knownForTitles"
# 11:"category"
# 12:"genres"
# 13:"budget"
# 14:"homepage"
# 15:"overview"
# 16:"production_countries"
# 17:"release_date"
# 18:"production_companies_name"
# 19:"url_complet"
# 20:"acteurs_id"
# 21:"jobs"
# 22:"noms"
# 23:"genres_list"
# ]

# 06/06/2025
#PROJET 2
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


# 06/06/2025
#PAGES

import streamlit as st
import pandas as pd
import plotly.express as px
import re

@st.cache_data
def load_data():
    return pd.read_csv("df_sans_vec.csv")

df_sans_vec = load_data()

def accueil():
    st.header(" 🎬 CINE PROJECT")
    # st.write(df_sans_vec["originalTitle"].head(20))
    # st.write(df_sans_vec.columns)
    # st.write(df_sans_vec["averageRating"])
    st.markdown(
        """
        Bienvenue sur <strong>CINE PROJECT</strong>, votre destination pour découvrir et explorer l'univers du cinéma.  
        Notre ADN repose sur la passion du 7<sup>ème</sup> art, le partage d'idées et l'inspiration.  
        Des recommandations qui vous correspondent grâce à une analyse ciblée du marché du cinéma français.  
        Des données mises à jour en temps réel en fonction des dernières sorties et avis du public,  
        exclusivement orientées selon les attentes des spectateurs français.
        """,
        unsafe_allow_html=True
    )

    # Visuel indicateur clé
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(
            """
            <h3 style='color:#1a73e8; font-size:36px; font-weight:bold; text-align:center;'>
                🎬 Nombre total de films disponibles : 17 000
            </h3>
            """,
            unsafe_allow_html=True
        )

    # === SECTION : GRAPHIQUES DYNAMIQUES ===
    st.header(" Analyse de l'évolution des Entrées en Salle")

    # Données 1 : par nationalité
    df1 = pd.DataFrame({
        'Année': list(range(2015, 2025)),
        'Films français': [90, 95, 97, 92, 89, 25, 35, 50, 65, 55],
        'Films américains': [110, 115, 100, 90, 115, 20, 30, 40, 50, 45],
        'Films européens': [20, 22, 25, 28, 20, 8, 12, 18, 20, 25],
        'Films autres nationalités': [5, 6, 7, 8, 4, 2, 4, 5, 6, 7]
    })

    # Données 2 : entrées totales
    df2 = pd.DataFrame({
        'Année': list(range(2007, 2025)),
        'Entrées (millions)': [178, 190, 201, 207, 217, 203, 193, 209, 205, 213,
                              209, 201, 213, 65, 95, 152, 180, 181]
    })

    # Graphique interactif 1
    df1_melted = df1.melt(id_vars='Année', var_name='Nationalité', value_name='Entrées')
    fig1 = px.line(df1_melted, x='Année', y='Entrées', color='Nationalité',
                   markers=True, title="Évolution des entrées en salle par nationalité (2015–2024)",
                   height=400)

    # Graphique interactif 2
    fig2 = px.bar(df2, x='Année', y='Entrées (millions)', text='Entrées (millions)',
                  title="Évolution des entrées totales en millions (2007-2025)", height=400)
    fig2.update_traces(textposition='outside')

    # Affichage des graphiques côte à côte
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
            """
            <h3 style='color:#1a73e8; font-weight:bold; margin-top: 10px;'>
                Les films français sont en vogue
            </h3>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            """
            <h3 style='color:#1a73e8; font-weight:bold; margin-top: 10px;'>
                📉 Reprise nette de la fréquentation après le COVID
            </h3>
            """,
            unsafe_allow_html=True
        )


# def recherche():
#     import streamlit as st
#     import pandas as pd

#     @st.cache_data
#     def load_data():
#         df = pd.read_csv("df_sans_vec.csv")
#         df = df[df['url_complet'].notna()]
#         df = df[df['startYear'].apply(lambda x: str(x).isdigit())]
#         df['startYear'] = df['startYear'].astype(int)
#         return df

#     df = load_data()

#     st.title("Espace Découverte de Films")

#     if "filtre_actif" not in st.session_state:
#         st.session_state.filtre_actif = None
#     if "titre_input" not in st.session_state:
#         st.session_state.titre_input = ""
#     if "genre_input" not in st.session_state:
#         st.session_state.genre_input = ""
#     if "nom" not in st.session_state:
#         st.session_state.nom = ""
#     if "page_num" not in st.session_state:
#         st.session_state.page_num = 0

#     if st.button("Réinitialiser les filtres"):
#         st.session_state.filtre_actif = None
#         st.session_state.titre_input = ""
#         st.session_state.genre_input = ""
#         st.session_state.nom = ""
#         st.session_state.page_num = 0
#         st.rerun()

#     def activer_filtre(nom):
#         st.session_state.filtre_actif = nom
#         st.session_state.page_num = 0

#     st.subheader("🔍 Recherche par titre de film")
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         titre_input = st.text_input("Titre du film", key="titre_input", placeholder="Tapez un titre...")
#     with col2:
#         st.button("Afficher", key="btn_titre", on_click=activer_filtre, args=("titre",))

#     st.subheader("🎞️ Recherche par genre")
#     genres_disponibles = sorted(df['genres'].dropna().unique())
#     col3, col4 = st.columns([4, 1])
#     with col3:
#         genre_input = st.selectbox("Choisir un genre", [""] + genres_disponibles, key="genre_input")
#     with col4:
#         st.button("Afficher", key="btn_genre", on_click=activer_filtre, args=("genre",))

#     st.subheader("🎭 Recherche par nom")
#     col5, col6 = st.columns([4, 1])
#     with col5:
#         nom_recherche = st.text_input("Nom de l'acteur, actrice ou réalisateur", key="nom", placeholder="Tapez un nom...")
#     with col6:
#         st.button("Afficher", key="btn_nom", on_click=activer_filtre, args=("nom",))

#     if st.session_state.filtre_actif == "titre" and titre_input:
#         df_filtre = df[df['originalTitle'].str.lower().str.contains(titre_input.lower(), na=False)]
#     elif st.session_state.filtre_actif == "genre" and genre_input:
#         df_filtre = df[df['genres'] == genre_input]
#     elif st.session_state.filtre_actif == "nom" and nom_recherche:
#         df_filtre = df[df['noms'].str.lower().str.contains(nom_recherche.lower(), na=False)]
#     else:
#         df_filtre = pd.DataFrame()

#     df_filtre = df_filtre.sort_values(by="startYear", ascending=False)
#     df_filtre = df_filtre[df_filtre['url_complet'].notna() & (df_filtre['url_complet'].str.strip() != "")]

#     page_size = 9  # 3 par ligne, 3 lignes
#     total_results = len(df_filtre)
#     total_pages = (total_results + page_size - 1) // page_size
#     page_num = st.session_state.page_num

#     start = page_num * page_size
#     end = start + page_size
#     page_data = df_filtre.iloc[start:end]

#     if not page_data.empty:
#         rows = [page_data[i:i+3] for i in range(0, len(page_data), 3)]
#         for row_chunk in rows:
#             cols = st.columns(3)
#             for idx, (_, row) in enumerate(row_chunk.iterrows()):
#                 with cols[idx]:
#                     st.image(row['url_complet'], width=300)
#                     st.markdown(f"**{row['originalTitle']}**")
#                     st.write(f"📅 Année : {row.get('startYear', 'Inconnu')}")
#                     st.write(f"🎞️ Genres : {row.get('genres', 'Non spécifié')}")

#         st.markdown(f"**Page {page_num + 1} sur {total_pages}**")
#         col_prev, col_next = st.columns(2)
#         with col_prev:
#             if page_num > 0 and st.button("⬅️ Page précédente"):
#                 st.session_state.page_num -= 1
#                 st.rerun()
#         with col_next:
#             if page_num < total_pages - 1 and st.button("➡️ Page suivante"):
#                 st.session_state.page_num += 1
#                 st.rerun()
#     else:
#         if st.session_state.filtre_actif:
#             st.warning("Aucun résultat trouvé pour ce filtre.")

# def recherche():
#     import streamlit as st
#     import pandas as pd

#     # Chargement des données
#     @st.cache_data
#     def load_data():
#         df = pd.read_csv("df_sans_vec.csv")
#         df = df[df['url_complet'].notna()]
#         df = df[df['startYear'].apply(lambda x: str(x).isdigit())]
#         df['startYear'] = df['startYear'].astype(int)
#         df = df.sort_values(by="startYear", ascending=False)
#         return df

#     df = load_data()
#     st.title("Espace Découverte de Films")

#     # Initialisation
#     for key, default in [("filtre_actif", None), ("titre_input", ""), ("genre_input", ""), ("nom", ""), ("page_num", 0)]:
#         if key not in st.session_state:
#             st.session_state[key] = default

#     # Réinitialisation
#     if st.button("Réinitialiser les filtres", key="reset_btn"):
#         for key in ["filtre_actif", "titre_input", "genre_input", "nom", "page_num"]:
#             if key in st.session_state:
#                 del st.session_state[key]
#         st.rerun()

#     def activer_filtre(nom):
#         st.session_state.filtre_actif = nom
#         st.session_state.page_num = 0

#     # 🔍 Recherche par titre
#     st.subheader("🔍 Recherche par titre de film")
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         titre_input = st.text_input("Titre du film", key="titre_input", placeholder="Tapez un titre...")
#     with col2:
#         st.button("Afficher", key="btn_titre", on_click=activer_filtre, args=("titre",))

#     # 🎞️ Recherche par genre
#     st.subheader("🎞️ Recherche par genre")
#     genres_dispo = sorted(df['genres'].dropna().unique())
#     col3, col4 = st.columns([4, 1])
#     with col3:
#         genre_input = st.selectbox("Choisir un genre", [""] + genres_dispo, key="genre_input")
#     with col4:
#         st.button("Afficher", key="btn_genre", on_click=activer_filtre, args=("genre",))

#     # 🎭 Recherche par nom
#     st.subheader("🎭 Recherche par nom")
#     col5, col6 = st.columns([4, 1])
#     with col5:
#         nom_input = st.text_input("Nom de l'acteur, actrice ou réalisateur", key="nom", placeholder="Tapez un nom...")
#     with col6:
#         st.button("Afficher", key="btn_nom", on_click=activer_filtre, args=("nom",))

#     # Appliquer les filtres
#     if st.session_state.filtre_actif == "titre" and titre_input:
#         df_filtre = df[df['originalTitle'].str.lower().str.contains(titre_input.lower(), na=False)]
#     elif st.session_state.filtre_actif == "genre" and genre_input:
#         df_filtre = df[df['genres'] == genre_input]
#     elif st.session_state.filtre_actif == "nom" and nom_input:
#         df_filtre = df[df['noms'].str.lower().str.contains(nom_input.lower(), na=False)]
#     else:
#         df_filtre = pd.DataFrame()

#     # Filtrage des images valides
#     df_filtre = df_filtre[df_filtre['url_complet'].notna() & (df_filtre['url_complet'].str.strip() != "")]
#     df_filtre = df_filtre.sort_values(by="startYear", ascending=False)

#     # Pagination
#     page_size = 9
#     total_results = len(df_filtre)
#     total_pages = (total_results + page_size - 1) // page_size
#     page_num = st.session_state.page_num

#     start = page_num * page_size
#     end = start + page_size
#     page_data = df_filtre.iloc[start:end]

#     # Résultats
#     if not page_data.empty:
#         rows = [page_data.iloc[i:i + 3] for i in range(0, len(page_data), 3)]
#         for ligne in rows:
#             cols = st.columns(3)
#             for idx, (_, row) in enumerate(ligne.iterrows()):
#                 with cols[idx]:
#                     st.image(row['url_complet'], width=300)
#                     st.markdown(f"**{row['originalTitle']}**")
#                     st.write(f"Année : {row['startYear']}")
#                     st.write(f"Genres : {row['genres']}")

#         # Navigation
#         st.write(f"Page {page_num + 1} sur {total_pages}")
#         col_prev, col_next = st.columns([1, 1])
#         with col_prev:
#             if page_num > 0 and st.button("⬅️ Page précédente"):
#                 st.session_state.page_num -= 1
#                 st.rerun()
#         with col_next:
#             if page_num < total_pages - 1 and st.button("➡️ Page suivante"):
#                 st.session_state.page_num += 1
#                 st.rerun()
#     else:
#         if st.session_state.filtre_actif:
#             st.warning("Aucun résultat trouvé.")



def recherche():
    # Chargement des données
    @st.cache_data
    def load_data():
        df = pd.read_csv("df_sans_vec.csv")
        df = df[df['url_complet'].notna()]
        df = df[df['startYear'].apply(lambda x: str(x).isdigit())]
        df['startYear'] = df['startYear'].astype(int)
        df = df.sort_values(by="startYear", ascending=False)
        return df

    print(st.session_state)

    # @st.cache_data
    # def load_data():
    #     df = pd.read_csv("df_sans_vec.csv")
    #     df.columns = df.columns.str.strip()
    #     df = df[df['url_complet'].notna()]
    #     df = df[df['url_complet'].str.strip() != ""]
    #     df = df[df['startYear'].apply(lambda x: str(x).isdigit())]
    #     df['startYear'] = df['startYear'].astype(int)
    #     df = df.sort_values(by="startYear", ascending=False)
    #     return df
        
    df = load_data()
    st.header(" 🎬 CINE PROJECT")
    st.title("🔎 Recherche de films")

    if "filtre_actif" not in st.session_state:
        st.session_state.filtre_actif = None
    if "titre_input" not in st.session_state:
        st.session_state.titre_input = ""
    if "genre_input" not in st.session_state:
        st.session_state.genre_input = ""
    if "nom" not in st.session_state:
        st.session_state.nom = ""
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    # Bouton de réinitialisation
    if st.button("Réinitialiser les filtres"):
        st.session_state.filtre_actif = None
        st.session_state.titre_input = ""
        st.session_state.genre_input = ""
        st.session_state.nom = ""
        st.session_state.page_num = 0
        st.experimental_rerun()

    # Fonctions pour activer les filtres
    def activer_filtre(nom):
        st.session_state.filtre_actif = nom
        st.session_state.page_num = 0

    # 🎬 Recherche par titre
    st.subheader("🎬 Par titre")
    col1, col2 = st.columns([4, 1])
    with col1:
        titre_input = st.text_input("Titre du film", key="titre_input")
    with col2:
        st.button("Rechercher", key="btn_titre", on_click=activer_filtre, args=("titre",))

    # 🎞️ Recherche par genre
    st.subheader("🎞️ Par genre")
    genres = sorted(df['genres'].dropna().unique())
    col1, col2 = st.columns([4, 1])
    with col1:
        genre_input = st.selectbox("Choisir un genre", [""] + genres, key="genre_input")
    with col2:
        st.button("Rechercher", key="btn_genre", on_click=activer_filtre, args=("genre",))

    # 🎭 Recherche par nom
    st.subheader("🎭 Par nom (acteur/réalisateur)")
    col1, col2 = st.columns([4, 1])
    with col1:
        nom_input = st.text_input("Nom", key="nom")
    with col2:
        st.button("Rechercher", key="btn_nom", on_click=activer_filtre, args=("nom",))

    # Application des filtres
    if st.session_state.filtre_actif == "titre" and titre_input:
        df_filtre = df[df['originalTitle'].str.lower().str.contains(titre_input.lower(), na=False)]
    elif st.session_state.filtre_actif == "genre" and genre_input:
        df_filtre = df[df['genres'] == genre_input]
    elif st.session_state.filtre_actif == "nom" and nom_input:
        df_filtre = df[df['noms'].str.lower().str.contains(nom_input.lower(), na=False)]
    else:
        df_filtre = pd.DataFrame()

    if not df_filtre.empty:
        df_filtre = df_filtre[df_filtre['url_complet'].notna()]
        df_filtre = df_filtre[df_filtre['url_complet'].str.strip() != ""]
        df_filtre = df_filtre.sort_values(by="startYear", ascending=False)

        # Pagination
        page_size = 9
        total_pages = (len(df_filtre) + page_size - 1) // page_size
        page_num = st.session_state.page_num
        start = page_num * page_size
        end = start + page_size
        page_data = df_filtre.iloc[start:end]

        # Affichage par lignes de 3
        for i in range(0, len(page_data), 3):
            cols = st.columns(3)
            for j, (_, row) in enumerate(page_data.iloc[i:i+3].iterrows()):
                with cols[j]:
                    st.image(row['url_complet'], width=300)
                    st.markdown(f"**{row['originalTitle']}**")
                    st.write(f"Année : {row['startYear']}")
                    st.write(f"Genres : {row['genres']}")
                    clicked = st.button("Accéder à la reco")
                    if clicked:
                        st.session_state["film_selectionne"] = row["original_title"]
                        st.session_state["page"] = "Reco"
                        st.rerun()

        # Navigation
        st.markdown(f"Page {page_num + 1} sur {total_pages}")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if page_num > 0 and st.button("⬅️ Page précédente"):
                st.session_state.page_num -= 1
                st.experimental_rerun()
        with col_next:
            if page_num < total_pages - 1 and st.button("➡️ Page suivante"):
                st.session_state.page_num += 1
                st.experimental_rerun()
    else:
        if st.session_state.filtre_actif:
            st.warning("Aucun résultat trouvé pour ce filtre.")


def espace_découverte():

    # Chargement des données
    @st.cache_data
    def load_data():
        df = pd.read_csv("df_sans_vec.csv")
        df = df[df['url_complet'].notna()]
        df = df[df['startYear'].apply(lambda x: str(x).isdigit())]
        df['startYear'] = df['startYear'].astype(int)
        df = df.sort_values(by="startYear", ascending=False)
        return df

    df = load_data()
    st.header(" 🎬 CINE PROJECT")
    st.title("Espace Découverte de Films")

    # Initialisation de la session
    if "filtre_actif" not in st.session_state:
        st.session_state.filtre_actif = None

    def activer_filtre(nom):
        st.session_state.filtre_actif = nom

    # 🎬 Derniers films par date
    st.subheader("🎬 Top 10 derniers films par date")
    col_date_1, col_date_2 = st.columns([3, 1])
    with col_date_1:
        tri_date = st.selectbox("Trier par année", ["", "Plus récent", "Plus ancien"], key="tri_date")
    with col_date_2:
        activer = st.button("Afficher", key="btn_date", on_click=activer_filtre, args=("date",))

    if st.session_state.filtre_actif == "date" and tri_date:
        df_sorted_date = df.sort_values(by="startYear", ascending=(tri_date == "Plus ancien"))
        film_ligne = df_sorted_date.head(10)
        cols = st.columns(10)
        for i, (_, row) in enumerate(film_ligne.iterrows()):
            with cols[i]:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=100)
                st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
                st.markdown(f"Genres : {row['genres']}")

    # ⭐ Meilleurs films par note
    st.subheader("⭐ Top 10 TOP-FLOP films par note")
    col_note_1, col_note_2 = st.columns([3, 1])
    with col_note_1:
        tri_rating = st.selectbox("Trier par note", ["", "Note décroissante", "Note croissante"], key="tri_rating")
    with col_note_2:
        activer = st.button("Afficher", key="btn_rating", on_click=activer_filtre, args=("rating",))

    if st.session_state.filtre_actif == "rating" and tri_rating:
        df_rating = df[df['averageRating'].notna()].copy()
        df_rating = df_rating.sort_values(by="averageRating", ascending=(tri_rating == "Note croissante"))
        film_ligne = df_rating.head(10)
        cols = st.columns(10)
        for i, (_, row) in enumerate(film_ligne.iterrows()):
            with cols[i]:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=100)
                st.markdown(f"**{row['originalTitle']}**")
                st.write(f"Note : {row['averageRating']}")
                st.write(f"Année : {row['startYear']}")

    # 🏢 Films par société de production
    st.subheader("🏢 Films par société de production")
    col_prod_1, col_prod_2 = st.columns([3, 1])
    with col_prod_1:
        production_choices = sorted(df['production_companies_name'].dropna().unique())
        production_filter = st.selectbox("Rechercher par société de production", [""] + production_choices, key="prod_filter")
    with col_prod_2:
        activer = st.button("Afficher", key="btn_prod", on_click=activer_filtre, args=("prod",))

    if st.session_state.filtre_actif == "prod" and production_filter:
        df_prod = df[df['production_companies_name'] == production_filter]
        film_ligne = df_prod.head(10)
        cols = st.columns(10)
        for i, (_, row) in enumerate(film_ligne.iterrows()):
            with cols[i]:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=100)
                st.markdown(f"**{row['originalTitle']}**")
                st.write(f"Année : {row['startYear']}")
                st.write(f"Genres : {row['genres']}")

    # 🎭 Recherche par nom
    st.subheader("🎭 Recherche par noms d'ac(teur)trice ou réalisa(teur)trice")
    col_nom_1, col_nom_2 = st.columns([4, 1])
    with col_nom_1:
        suggestions = sorted(df['noms'].dropna().unique())
        nom_recherche = st.text_input("Nom de l'acteur, actrice ou réalisateur", key="nom", placeholder="Tapez un nom...")
    with col_nom_2:
        activer = st.button("Afficher", key="btn_nom", on_click=activer_filtre, args=("nom",))

    if st.session_state.filtre_actif == "nom" and nom_recherche:
        df_people = df[df['noms'].str.lower().str.contains(nom_recherche.lower(), na=False)]
        film_ligne = df_people.head(10)
        cols = st.columns(10)
        for i, (_, row) in enumerate(film_ligne.iterrows()):
            with cols[i]:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=100)
                st.markdown(f"**{row['originalTitle']}**")
                st.write(f"{row['noms']}")
                st.write(f"Année : {row['startYear']}")










import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("df_sans_vec.csv")

df_sans_vec = load_data()

def accueil():
    st.header(" 🎬 CINE PROJECT")
    st.write(df_sans_vec.columns)

    # Visuel indicateur clé
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(
            """
            <h3 style='color:#1a73e8; font-size:36px; font-weight:bold; text-align:center;'>
                🎬 Nombre total de films disponibles : 17 000
            </h3>
            """,
            unsafe_allow_html=True
        )

    # === SECTION : GRAPHIQUES DYNAMIQUES ===
    st.header(" Analyse de l'évolution des Entrées en Salle")

def recherche(df):
    st.header("🎬 CINE PROJECT")
    st.dataframe(df_sans_vec)
    st.write(df_sans_vec.columns)
# --- Page principale : recherche
    
    if "page" not in st.session_state:
        st.session_state.page = "recherche"

    if st.session_state.page == "recherche":
        st.title("🎬 Recherche de films")

        titre = st.text_input("🔍 Rechercher un film par nom")
        genres_uniques = sorted(set(g for sub in df_sans_vec["genres"].dropna().str.split(",") for g in sub))
        genres_sel = st.multiselect("🎞️ Sélectionner un ou plusieurs genres", genres_uniques)
        annees = sorted(df_sans_vec["startYear"].dropna().unique())
        annee_sel = st.selectbox("📅 Choisir l'année de sortie", annees)
        note_min = st.slider("⭐ Note moyenne minimum", 
                            min_value=float(df_sans_vec["average_rating"].min()), 
                            max_value=float(df_sans_vec["average_rating"].max()), 
                            value=float(df_sans_vec["average_rating"].min()))

    # --- Filtrage
    df_resultats = df_sans_vec.copy()

    if titre:
        df_resultats = df_resultats[df_resultats["title"].str.contains(titre, case=False, na=False)]

    if genres_sel:
        df_resultats = df_resultats[df_resultats["genres"].apply(
            lambda x: any(g in x for g in genres_sel) if pd.notna(x) else False
        )]

    if annee_sel:
        df_resultats = df_resultats[df_resultats["startYear"] == annee_sel]

    df_resultats = df_resultats[df_resultats["average_rating"] >= note_min]

    st.markdown("### 🎯 Résultats")
    for idx, row in df_resultats.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{row['title']}** ({row['startYear']}) - ⭐ {row['average_rating']}")
            st.caption(f"Genres : {row['genres']}")
        with col2:
            if st.button("Voir", key=f"btn_{idx}"):
                st.session_state.page = "details"
                st.session_state.film_selectionne = row.to_dict()
                st.experimental_rerun()

# --- Page détail film
elif st.session_state.page == "details":
    film = st.session_state.film_selectionne
    st.title(film["title"])
    st.image(film["url_complet"], use_column_width=True)
    st.markdown(f"**Année** : {film['startYear']}")
    st.markdown(f"**Genres** : {film['genres']}")
    st.markdown(f"**Note moyenne** : ⭐ {film['average_rating']}")
    if st.button("🔙 Retour aux résultats"):
        st.session_state.page = "recherche"
        st.rerun()























#version2
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Lire le fichier CSV (placé dans le même dossier que ce script)
df = pd.read_csv("df_fin_copy.csv")

# Affichage simple sans titre
# st.dataframe(df)

# Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche", "Nos recommandations"],
        icons=["film", "search", "stars"],
        menu_icon="camera-reels",
        default_index=0
         )

# # Sélection Accueil  
# if selection == "Accueil":
#     st.header(" 🎬 CINE PROJECT")
#     st.subheader("Notre ADN")
#     st.write("""
#         Bienvenue sur **CINE PROJECT**, votre destination pour découvrir et explorer l'univers du cinéma !  
#         Notre ADN repose sur la passion du 7ème art, le partage d'idées et l'inspiration. 
#         Des recommandations qui vous correspondent grâce à une analyse ciblée du marché du cinéma français. 
#         Des données mises à jour en temps réel en fonction des dernières sorties et avis du public, exclusivement orienté en fonction des
#         attentes des spectateurs français. 
#     """)

#     # Visuel indicateur clé
#     col1, col2, col3 = st.columns([1, 4, 1])
#     with col2:
#         st.markdown(
#             """
#             <h3 style='color:#1a73e8; font-size:36px; font-weight:bold; text-align:center;'>
#                 🎬 Nombre total de films disponibles : 17 000
#             </h3>
#             """,
#             unsafe_allow_html=True
#         )

#     # Images
#     st.image("fond_ecran.png", caption="Le cinéma, notre passion", width=200)

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # === SECTION : GRAPHIQUES DYNAMIQUES ===

# st.header(" Analyse de l'évolution des Entrées en Salle")

# # Données 1 : par nationalité
# df1 = pd.DataFrame({
#     'Année': list(range(2015, 2025)),
#     'Films français': [90, 95, 97, 92, 89, 25, 35, 50, 65, 55],
#     'Films américains': [110, 115, 100, 90, 115, 20, 30, 40, 50, 45],
#     'Films européens': [20, 22, 25, 28, 20, 8, 12, 18, 20, 25],
#     'Films autres nationalités': [5, 6, 7, 8, 4, 2, 4, 5, 6, 7]
# })

# # Données 2 : entrées totales
# df2 = pd.DataFrame({
#     'Année': list(range(2007, 2025)),
#     'ntrées (en millions)': [178, 190, 201, 207, 217, 203, 193, 209, 205, 213,
#                            209, 201, 213, 65, 95, 152, 180, 181]
# })

# # Graphique interactif 1
# df1_melted = df1.melt(id_vars='Année', var_name='Nationalité', value_name='Entrées')
# fig1 = px.line(df1_melted, x='Année', y='Entrées', color='Nationalité',
#                markers=True, title="Évolution des entrées en salle par nationalité (2015–2024)")

# # Graphique interactif 2
# fig2 = px.bar(df2, x='Année', y='Entrées (millions)', text='Entrées (millions)',
#               title="Évolution des entrées totales en millions (2007-2025)")
# fig2.update_traces(textposition='outside')

# # Affichage dans Streamlit
# col1, col2 = st.columns(2)
# with col1:
#     st.plotly_chart(fig1, use_container_width=True)
#     st.caption("📈 Les films français sont en vogue")

# with col2:
#     st.plotly_chart(fig2, use_container_width=True)
#     st.caption("📉 Reprise nette de la fréquentation après le COVID")


# Affichage dans Streamlit avec interprétations stylisées
# col1, col2 = st.columns(2)

# with col1:
#     st.plotly_chart(fig1, use_container_width=True)
#     st.markdown(
#         """
#         <div style='padding: 1em; background-color: #eaf4fc; border-left: 6px solid #1f77b4; border-radius: 8px; margin-top: 10px;'>
#             <h4 style='color: #1f77b4; font-size: 22px; margin: 0;'>📈 Les films français sont en vogue</h4>
#             <p style='margin: 0; font-size: 16px;'>Une tendance constante depuis plusieurs années.</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# with col2:
#     st.plotly_chart(fig2, use_container_width=True)
#     st.markdown(
#         """
#         <div style='padding: 1em; background-color: #fff3cd; border-left: 6px solid #ffc107; border-radius: 8px; margin-top: 10px;'>
#             <h4 style='color: #856404; font-size: 22px; margin: 0;'>📉 Reprise nette de la fréquentation après le COVID</h4>
#             <p style='margin: 0; font-size: 16px;'>Le public retourne progressivement dans les salles obscures.</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

import streamlit as st
import pandas as pd
import plotly.express as px

# Sélection Accueil  
if selection == "Accueil":
    st.header(" 🎬 CINE PROJECT")
    st.subheader("Notre ADN")
    st.write("""
        Bienvenue sur **CINE PROJECT**, votre destination pour découvrir et explorer l'univers du cinéma !  
        Notre ADN repose sur la passion du 7ème art, le partage d'idées et l'inspiration. 
        Des recommandations qui vous correspondent grâce à une analyse ciblée du marché du cinéma français. 
        Des données mises à jour en temps réel en fonction des dernières sorties et avis du public, exclusivement orienté en fonction des
        attentes des spectateurs français. 
    """)

    # Visuel indicateur clé
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(
            """
            <h3 style='color:#1a73e8; font-size:36px; font-weight:bold; text-align:center;'>
                🎬 Nombre total de films disponibles : 17 000
            </h3>
            """,
            unsafe_allow_html=True
        )

    # Images
    st.image("fond_ecran.png", caption="Le cinéma, notre passion", width=200)

    # === SECTION : GRAPHIQUES DYNAMIQUES ===
    st.header(" Analyse de l'évolution des Entrées en Salle")

    # Données 1 : par nationalité
    df1 = pd.DataFrame({
        'Année': list(range(2015, 2025)),
        'Films français': [90, 95, 97, 92, 89, 25, 35, 50, 65, 55],
        'Films américains': [110, 115, 100, 90, 115, 20, 30, 40, 50, 45],
        'Films européens': [20, 22, 25, 28, 20, 8, 12, 18, 20, 25],
        'Films autres nationalités': [5, 6, 7, 8, 4, 2, 4, 5, 6, 7]
    })

    # Données 2 : entrées totales
    df2 = pd.DataFrame({
        'Année': list(range(2007, 2025)),
        'Entrées (millions)': [178, 190, 201, 207, 217, 203, 193, 209, 205, 213,
                              209, 201, 213, 65, 95, 152, 180, 181]
    })

    # Graphique interactif 1
    df1_melted = df1.melt(id_vars='Année', var_name='Nationalité', value_name='Entrées')
    fig1 = px.line(df1_melted, x='Année', y='Entrées', color='Nationalité',
                   markers=True, title="Évolution des entrées en salle par nationalité (2015–2024)")

    # Graphique interactif 2
    fig2 = px.bar(df2, x='Année', y='Entrées (millions)', text='Entrées (millions)',
                  title="Évolution des entrées totales en millions (2007-2025)")
    fig2.update_traces(textposition='outside')

    # Affichage combiné dans Streamlit avec interprétations stylisées
    col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        """
        <h3 style='color:#1a73e8; font-weight:bold; margin-top: 10px;'>
            📈 Les films français sont en vogue
        </h3>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        """
        <h3 style='color:#1a73e8; font-weight:bold; margin-top: 10px;'>
            📉 Reprise nette de la fréquentation après le COVID
        </h3>
        """,
        unsafe_allow_html=True
    )




    # col1, col2 = st.columns(2)
    # with col1:
    #     st.image("entrees_nationalite.jpg", caption="Les films français sont en vogue", width=500)
    # with col2:
    #     st.image("evolution_entrees.jpg", caption="Reprise nette de la fréquentation après le COVID", width=500)

# Sélection Recherche  
# elif selection == "Recherche":
#     st.subheader("Rechercher un film")

#     query = st.text_input("Tapez un titre (original ou localisé) :")
#     if query:
#         mask = df['originalTitle'].str.contains(query, case=False) | df['primaryTitle'].str.contains(query, case=False)
#         results = df[mask].head(10)

#         if not results.empty:
#             st.write("Voici les suggestions :")

#             titles = [f"{row['primaryTitle']} (Original: {row['originalTitle']})" for _, row in results.iterrows()]
#             choice = st.selectbox("Sélectionnez un film pour voir sa page :", titles)

#             selected_row = results.iloc[titles.index(choice)]
#             url = selected_row['url_complet']

#             st.write(f"Affichage de la page pour : **{choice}**")
#             components.iframe(url, height=600)
#         else:
#             st.warning("Aucun film trouvé.")
#     else:
#         st.info("Commencez à taper pour voir des suggestions.")


if selection == "Recherche":
    st.header(" 🎬 CINE PROJECT")
    st.subheader("Rechercher un film")

    query = st.text_input("Tapez un titre (original ou localisé) :")

    if query:
        mask = df['originalTitle'].str.contains(query, case=False) | df['primaryTitle'].str.contains(query, case=False)
        results = df[mask].head(25)  # limite totale max 25 résultats pour gérer 5 par ligne * 5 lignes max

        if not results.empty:
            st.write("Voici les suggestions :")

            films_per_row = 5
            rows = (len(results) + films_per_row - 1) // films_per_row  # nombre de lignes nécessaires

            for row_idx in range(rows):
                start_idx = row_idx * films_per_row
                end_idx = start_idx + films_per_row
                row_films = results.iloc[start_idx:end_idx]

                cols = st.columns(len(row_films))  # créer autant de colonnes que de films dans la ligne

                for col, (_, film) in zip(cols, row_films.iterrows()):
                    with col:
                        st.image(film['url_complet'], width=150)
                        st.markdown(f"**{film['primaryTitle']}**")
                        st.markdown(f"*Original: {film['originalTitle']}*")
                        # Optionnel, lien cliquable sur l'image ou le titre :
                        # st.markdown(f"[Voir la page]({film['url_complet']})")
                st.markdown("---")  # séparation entre lignes
        else:
            st.warning("Aucun film trouvé.")

else:
    st.info("Commencez à taper pour voir des suggestions.")

if "recherche_genre" not in st.session_state:
    st.session_state.recherche_genre = None

if st.session_state.recherche_genre is None:
    st.header("🎥 Une envie particulière ?")

    col1, col2, col3 = st.columns([3, 2, 3])
    with col1:
        recherche = st.text_input("", placeholder="Tapez un nom, une star, un genre, un utilisateur...").strip().lower()

    if recherche == "avatar":
        st.image("avatar.png", caption="Avatar")
        st.subheader("Descriptif :")
        st.write("""...""")
            
    # else:
    #     st.info("Commencez à taper pour voir des suggestions.")

    # # elif selection == "Recherche":
    # elif "recherche_genre" not in st.session_state:
    #     st.session_state.recherche_genre = None

    # # Si aucun genre sélectionné, affichage de la recherche générale + filtres
    # elif st.session_state.recherche_genre is None:
    #     st.header("🎥 Une envie particulière ?")

    #     col1, col2, col3 = st.columns([3, 2, 3])
    #     with col1:
    #         recherche = st.text_input("", placeholder="Tapez un nom, une star, un genre, un utilisateur...").strip().lower()

    #     if recherche == "avatar":
    #         st.image("avatar.png", caption="Avatar")
    #         st.subheader("Descriptif :")
    #         st.write("""
    #         - **Titre** : Avatar  
    #         - **Réalisateur** : James Cameron  
    #         - **Année de sortie** : 2009  
    #         - **Genre** : Science-fiction, Aventure  
    #         - **Synopsis** : Sur la planète Pandora, un ex-marine est impliqué dans un conflit épique opposant humains et Na'vi.
    #         """)
    #         st.subheader("Avis des spectateurs :")
    #         st.write("🌟🌟🌟🌟🌟 - Un chef d'œuvre visuel et narratif, une aventure inoubliable.")
    #         st.subheader("Note spectateur :")
    #         st.write("⭐️ 4.8 / 5")

    #     elif recherche == "wish":
    #         st.image("wish.png", caption="Wish")
    #         st.subheader("Descriptif :")
    #         st.write("""
    #         - **Titre** : Wish 
    #         - **Durée** : 1h 42min  
    #         - **Public** : à partir de 6 ans  
    #         - **Réalisateur** : Chris Buck, Fawn Veerasunthorn
    #         - **Acteurs principaux** : Océane Demontis, Ariana DeBose, Chris Pine         
    #         - **Année de sortie** : 2023  
    #         - **Genre** : Aventure, Animation, Famille  
    #         - **Synopsis** : Jeune fille de 17 ans à l’esprit vif, Asha vit à Rosas, un royaume fantastique où tous les souhaits peuvent littéralement s’exaucer. Elle adresse un vœu sincère et puissant aux étoiles auquel va répondre une force cosmique : une petite boule d’énergie infinie prénommée Star, peut réellement produire des miracles....
    #         """)
    #         st.subheader("Avis des spectateurs :")
    #         st.write("🌟🌟🌟 - Magique, inoubliable")
    #         st.subheader("Note spectateur :")
    #         st.write("⭐️ 3,5 / 5")

    #     elif recherche != "":
    #         st.warning("Film non trouvé. Essayez 'AVATAR'.")

    #     st.subheader("🎞️ Filtrer par genre :")
    #     genres = ["Jeunesse", "Aventure", "Science-Fiction", "Comédies", "Documentaires", "Drama", "Intrigue-Suspens", "Romantique"]
    #     genre_cols = st.columns(4)
    #     for i, genre in enumerate(genres):
    #         if genre_cols[i % 4].button(genre):
    #             st.session_state.recherche_genre = genre
    #             st.rerun()

    # # Affichage spécifique à un genre
    # else:
    #     genre = st.session_state.recherche_genre
    #     st.header(f"🎬 Genre sélectionné : {genre}")
    #     recherche_genre = st.text_input(f"🔍 Rechercher dans {genre}", placeholder="Tapez un titre, acteur, mot-clé...").strip().lower()

    #     st.subheader("⭐ Suggestions dans ce genre :")

    #     genre_images = {
    #         "Jeunesse": ["encanto.png"],
    #         "Aventure": ["vaiana.png"],
    #         "Science-Fiction": ["avatar.png"],
    #         "Comédies": ["wish.png"],
    #         "Documentaires": ["raya.png"],
    #         "Drama": ["lilostich.png"],
    #         "Intrigue-Suspens": ["encanto.png", "raya.png"],
    #         "Romantique": ["wish.png", "vaiana.png"]
    #     }

    #     for img in genre_images.get(genre, []):
    #         st.image(img, caption=img.replace(".png", "").capitalize())

    #     if recherche_genre:
    #         st.info(f"Recherche dans **{genre}** pour : **{recherche_genre}**")

    #     if st.button("⬅ Retour aux filtres"):
    #         st.session_state.recherche_genre = None
    #         st.rerun()







elif selection == "Nos recommandations":
    st.header(" 🎬 CINE PROJECT")
    # Initialisation de la page interne "Besoin d'idées"
    if "idee_page" not in st.session_state:
        st.session_state.idee_page = "themes"

    # Affichage des boutons de thématiques
    if st.session_state.idee_page == "themes":
        st.header("🌟 Besoin d'idées ?")
        st.write("""
            Découvrez nos suggestions et recommandations pour enrichir votre expérience cinématographique.  
            Nous mettons à jour nos idées régulièrement, restez connectés !
        """)
        st.subheader("Choisissez une thématique :")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Top films populaires".upper()):
                st.session_state.idee_page = "populaires"
            if st.button("Top meilleures critiques".upper()):
                st.session_state.idee_page = "critiques"
            if st.button("Top célébrités".upper()):
                st.session_state.idee_page = "célébrités"

        with col2:
            if st.button("À l'affiche".upper()):
                st.session_state.idee_page = "affiche"
            if st.button("Films cultes".upper()):
                st.session_state.idee_page = "cultes"
            if st.button("Les sagas".upper()):
                st.session_state.idee_page = "sagas"

    # Affichage des recommandations selon le thème sélectionné
    else:
        theme = st.session_state.idee_page
        st.header(f"🎬 Thématique : {theme.capitalize()}")
        recherche = st.text_input("🔍 Rechercher un film", placeholder="Tapez un titre ou un genre...")

        st.subheader("⭐ Suggestions de films :")

        theme_images = {
            "populaires": ["avatar.png", "wish.png"],
            "critiques": ["encanto.png"],
            "célébrités": ["vaiana.png"],
            "affiche": ["raya.png"],
            "cultes": ["lilostich.png"],
            "sagas": ["avatar.png", "vaiana.png"]
        }

        for img in theme_images.get(theme, []):
            st.image(img, caption=img.replace(".png", "").capitalize())

        if recherche:
            st.info(f"Vous avez recherché : **{recherche}**")

        if st.button("⬅ Retour"):
            st.session_state.idee_page = "themes"







#Version 1



import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

st.set_page_config(layout="wide", page_title="CINE PROJECT", page_icon="🎬")

# @st.cache_data
# def load_data():
#     return pd.read_csv("Feuil1.csv")

# df = load_data()
# #pleine page
# st.set_page_config(layout="wide")
# films = [
#     {"titre": "Avatar", "genre": "Science-Fiction", "acteur": "Sam Worthington", "image": "avatar.png"},
#     {"titre": "Wish", "genre": "Aventure", "acteur": "Ariana DeBose", "image": "wish.png"},
#     {"titre": "Vaiana", "genre": "Aventure", "acteur": "Auli'i Cravalho", "image": "vaiana.png"},
# ]
# # Titre principal
# st.title("🎬 CINE PROJECT")

# Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche", "Nos recommandations"],
        icons=["film", "search", "stars"],
        menu_icon="camera-reels",
        default_index=0
         )

# Sélection Accueil  
if selection == "Accueil":
    st.header("Notre site")
    st.subheader("Notre ADN")
    st.write("""
        Bienvenue sur **CINE PROJECT**, votre destination pour découvrir et explorer l'univers du cinéma !  
        Notre ADN repose sur la passion du 7ème art, le partage d'idées et l'inspiration.
    """)

    # Visuel de type Power BI : indicateur clé
    st.markdown("### 📊 Notre base de données")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(label="🎬 Nombre total de films disponibles", value="17 000")

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown(
        """
        <h3 style='color:#1a73e8; font-size:36px; font-weight:bold; text-align:center;'>
            🎬 Nombre total de films disponibles : 17 000
        </h3>
        """,
        unsafe_allow_html=True
    )




    # Images
    st.image("fond_ecran.png", caption="Le cinéma, notre passion", width=600)

    col1, col2 = st.columns(2)
    with col1:
        st.image("entrees_nationalite.jpg", caption="Les films français sont en vogue", width=500)
    with col2:
        st.image("evolution_entrees.jpg", caption="Reprise nette de la fréquentation après le COVID", width=500)

# Sélection Recherche  
elif selection == "Recherche":
    if "recherche_genre" not in st.session_state:
        st.session_state.recherche_genre = None

    # Si aucun genre sélectionné, affichage de la recherche générale + filtres
    if st.session_state.recherche_genre is None:
        st.header("🎥 Une envie particulière ?")

        col1, col2, col3 = st.columns([3, 2, 3])
        with col1:
            recherche = st.text_input("", placeholder="Tapez un nom, une star, un genre, un utilisateur...").strip().lower()

        if recherche == "avatar":
            st.image("avatar.png", caption="Avatar")
            st.subheader("Descriptif :")
            st.write("""
            - **Titre** : Avatar  
            - **Réalisateur** : James Cameron  
            - **Année de sortie** : 2009  
            - **Genre** : Science-fiction, Aventure  
            - **Synopsis** : Sur la planète Pandora, un ex-marine est impliqué dans un conflit épique opposant humains et Na'vi.
            """)
            st.subheader("Avis des spectateurs :")
            st.write("🌟🌟🌟🌟🌟 - Un chef d'œuvre visuel et narratif, une aventure inoubliable.")
            st.subheader("Note spectateur :")
            st.write("⭐️ 4.8 / 5")

        elif recherche == "wish":
            st.image("wish.png", caption="Wish")
            st.subheader("Descriptif :")
            st.write("""
            - **Titre** : Wish 
            - **Durée** : 1h 42min  
            - **Public** : à partir de 6 ans  
            - **Réalisateur** : Chris Buck, Fawn Veerasunthorn
            - **Acteurs principaux** : Océane Demontis, Ariana DeBose, Chris Pine         
            - **Année de sortie** : 2023  
            - **Genre** : Aventure, Animation, Famille  
            - **Synopsis** : Jeune fille de 17 ans à l’esprit vif, Asha vit à Rosas, un royaume fantastique où tous les souhaits peuvent littéralement s’exaucer. Elle adresse un vœu sincère et puissant aux étoiles auquel va répondre une force cosmique : une petite boule d’énergie infinie prénommée Star, peut réellement produire des miracles....
            """)
            st.subheader("Avis des spectateurs :")
            st.write("🌟🌟🌟 - Magique, inoubliable")
            st.subheader("Note spectateur :")
            st.write("⭐️ 3,5 / 5")

        elif recherche != "":
            st.warning("Film non trouvé. Essayez 'AVATAR'.")

        st.subheader("🎞️ Filtrer par genre :")
        genres = ["Jeunesse", "Aventure", "Science-Fiction", "Comédies", "Documentaires", "Drama", "Intrigue-Suspens", "Romantique"]
        genre_cols = st.columns(4)
        for i, genre in enumerate(genres):
            if genre_cols[i % 4].button(genre):
                st.session_state.recherche_genre = genre
                st.rerun()

    # Affichage spécifique à un genre
    else:
        genre = st.session_state.recherche_genre
        st.header(f"🎬 Genre sélectionné : {genre}")
        recherche_genre = st.text_input(f"🔍 Rechercher dans {genre}", placeholder="Tapez un titre, acteur, mot-clé...").strip().lower()

        st.subheader("⭐ Suggestions dans ce genre :")

        genre_images = {
            "Jeunesse": ["encanto.png"],
            "Aventure": ["vaiana.png"],
            "Science-Fiction": ["avatar.png"],
            "Comédies": ["wish.png"],
            "Documentaires": ["raya.png"],
            "Drama": ["lilostich.png"],
            "Intrigue-Suspens": ["encanto.png", "raya.png"],
            "Romantique": ["wish.png", "vaiana.png"]
        }

        for img in genre_images.get(genre, []):
            st.image(img, caption=img.replace(".png", "").capitalize())

        if recherche_genre:
            st.info(f"Recherche dans **{genre}** pour : **{recherche_genre}**")

        if st.button("⬅ Retour aux filtres"):
            st.session_state.recherche_genre = None
            st.rerun()

elif selection == "Nos recommandations":

    # Initialisation de la page interne "Besoin d'idées"
    if "idee_page" not in st.session_state:
        st.session_state.idee_page = "themes"

    # Affichage des boutons de thématiques
    if st.session_state.idee_page == "themes":
        st.header("🌟 Besoin d'idées ?")
        st.write("""
            Découvrez nos suggestions et recommandations pour enrichir votre expérience cinématographique.  
            Nous mettons à jour nos idées régulièrement, restez connectés !
        """)
        st.subheader("Choisissez une thématique :")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Top films populaires".upper()):
                st.session_state.idee_page = "populaires"
            if st.button("Top meilleures critiques".upper()):
                st.session_state.idee_page = "critiques"
            if st.button("Top célébrités".upper()):
                st.session_state.idee_page = "célébrités"

        with col2:
            if st.button("À l'affiche".upper()):
                st.session_state.idee_page = "affiche"
            if st.button("Films cultes".upper()):
                st.session_state.idee_page = "cultes"
            if st.button("Les sagas".upper()):
                st.session_state.idee_page = "sagas"

    # Affichage des recommandations selon le thème sélectionné
    else:
        theme = st.session_state.idee_page
        st.header(f"🎬 Thématique : {theme.capitalize()}")
        recherche = st.text_input("🔍 Rechercher un film", placeholder="Tapez un titre ou un genre...")

        st.subheader("⭐ Suggestions de films :")

        theme_images = {
            "populaires": ["avatar.png", "wish.png"],
            "critiques": ["encanto.png"],
            "célébrités": ["vaiana.png"],
            "affiche": ["raya.png"],
            "cultes": ["lilostich.png"],
            "sagas": ["avatar.png", "vaiana.png"]
        }

        for img in theme_images.get(theme, []):
            st.image(img, caption=img.replace(".png", "").capitalize())

        if recherche:
            st.info(f"Vous avez recherché : **{recherche}**")

        if st.button("⬅ Retour"):
            st.session_state.idee_page = "themes"