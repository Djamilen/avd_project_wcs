import streamlit as st
import pandas as pd
import plotly.express as px
import re

@st.cache_data
def load_data():
    return pd.read_csv("df_descriptif.csv")

reco_film = load_data()

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

def recherche():
    # Chargement des données
    @st.cache_data
    def load_data():
        df = pd.read_csv("df_descriptif.csv")
        df = df[df['url_complet'].notna()]
        df = df[df['startYear'].apply(lambda x: str(x).isdigit())]
        df['startYear'] = df['startYear'].astype(int)
        df = df.sort_values(by="startYear", ascending=False)
        return df



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
        st.rerun()

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

        # Navigation
        st.markdown(f"Page {page_num + 1} sur {total_pages}")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if page_num > 0 and st.button("⬅️ Page précédente"):
                st.session_state.page_num -= 1
                st.rerun()
        with col_next:
            if page_num < total_pages - 1 and st.button("➡️ Page suivante"):
                st.session_state.page_num += 1
                st.rerun()
    else:
        if st.session_state.filtre_actif:
            st.warning("Aucun résultat trouvé pour ce filtre.")


def espace_découverte():

    # Chargement des données
    @st.cache_data
    def load_data():
        df = pd.read_csv("df_descriptif.csv")
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
