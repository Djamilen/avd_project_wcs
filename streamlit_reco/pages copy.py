def espace_decouverte():
    import streamlit as st
    import pandas as pd

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

    st.title("Espace Découverte de Films")

    # Initialisation de la session
    if "filtre_actif" not in st.session_state:
        st.session_state.filtre_actif = None

    def activer_filtre(nom):
        st.session_state.filtre_actif = nom

    # 🎬 Derniers films par date
    st.subheader("🎬 Derniers films par date")
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
    st.subheader("⭐ Meilleurs films par note")
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
    st.subheader("🎭 Recherche par nom")
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

#VERSION 4

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

    df = load_data()
    st.header(" 🎬 CINE PROJECT")
    # Initialisation session state
    if "titre_input" not in st.session_state:
        st.session_state.titre_input = ""
    if "genre_selectionne" not in st.session_state:
        st.session_state.genre_selectionne = ""
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    # Titre de l'application
    st.title("Recherche de Films")

    # Barre de recherche + Réinitialisation côte à côte
    col1, col2 = st.columns([3, 1])
    with col1:
        titre_input = st.text_input("Titre du film", value=st.session_state.titre_input)
    with col2:
        if st.button("Réinitialiser le filtre"):
            st.session_state.titre_input = ""
            st.session_state.genre_selectionne = ""
            st.session_state.page_num = 0
            st.rerun()

    # Sélection du genre
    genres_disponibles = sorted(df['genres'].dropna().unique())
    genre_selectionne = st.selectbox(
        "Choisir un genre",
        [""] + genres_disponibles,
        index=([""] + genres_disponibles).index(st.session_state.genre_selectionne)
        if st.session_state.genre_selectionne in genres_disponibles else 0
    )

    # Bouton de recherche
    if st.button("Rechercher"):
        st.session_state.titre_input = titre_input
        st.session_state.genre_selectionne = genre_selectionne
        st.session_state.page_num = 0
        st.rerun()

    # Filtrage
    df_filtre = df.copy()
    if st.session_state.titre_input:
        recherche = st.session_state.titre_input.lower()
        df_filtre = df_filtre[df_filtre["originalTitle"].str.lower().str.contains(recherche)]
    if st.session_state.genre_selectionne:
        df_filtre = df_filtre[df_filtre["genres"] == st.session_state.genre_selectionne]

    df_filtre = df_filtre.sort_values(by="startYear", ascending=False)

# Supprimer les films sans image
    df_filtre = df_filtre[df_filtre["url_complet"].notna() & (df_filtre["url_complet"].str.strip() != "")]

    # Pagination
    page_size = 20
    total_results = len(df_filtre)
    total_pages = (total_results + page_size - 1) // page_size
    page_num = st.session_state.page_num

    start = page_num * page_size
    end = start + page_size
    page_data = df_filtre.iloc[start:end]

    # Affichage des films
    for _, row in page_data.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                poster = row.get("url_complet", "")
                if poster.strip():
                    st.image(poster, width=150)
                else:
                    st.warning("🖼️ Image non disponible.")
            with col2:
                st.subheader(row.get("originalTitle", "Titre inconnu"))
                st.markdown(f"**Genre :** {row.get('genres', 'Non spécifié')}")
                st.markdown(f"**Description :** {row.get('overview', 'Aucune description')}")

    # Navigation
    st.write(f"Page {page_num + 1} sur {total_pages}")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if page_num > 0 and st.button("⬅️ Page précédente"):
            st.session_state.page_num -= 1
            st.rerun()
    with col_next:
        if page_num < total_pages - 1 and st.button("➡️ Page suivante"):
            st.session_state.page_num += 1
            st.rerun()

def espace_decouverte():
    df = load_data()

    st.title("Espace Découverte de Films")

    # Section 1 - Derniers films par date
    st.subheader("🎬 Derniers films par date")
    col1, col2 = st.columns(2)
    with col1:
        tri_date = st.selectbox("Trier par année", ["Plus récent", "Plus ancien"])
    with col2:
        st.markdown("**OU**")

    df_sorted_date = df.sort_values(by="startYear", ascending=(tri_date == "Plus ancien"))
    films_date = df_sorted_date.head(10)
    cols = st.columns(10)
    for i, (_, row) in enumerate(films_date.iterrows()):
        with cols[i]:
            if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                st.image(row['url_complet'], width=100)
            st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
            st.caption(f"{row['genres']}")

    # Section 2 - Meilleurs films par note
    st.subheader("⭐ Meilleurs films par note")
    col3, col4 = st.columns(2)
    with col3:
        tri_rating = st.selectbox("Trier par note", ["Note décroissante", "Note croissante"])
    with col4:
        st.markdown("**OU**")

    df_rating = df[df['averageRating'].notna()].copy()
    df_rating = df_rating.sort_values(by="averageRating", ascending=(tri_rating == "Note croissante"))
    films_rating = df_rating.head(10)
    cols = st.columns(10)
    for i, (_, row) in enumerate(films_rating.iterrows()):
        with cols[i]:
            if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                st.image(row['url_complet'], width=100)
            st.markdown(f"**{row['originalTitle']}**")
            st.caption(f"⭐ {row['averageRating']} | {row['startYear']}")

    # Section 3 - Films par société de production
    st.subheader("🏢 Films par société de production")
    col5, col6 = st.columns(2)
    with col5:
        prod_choices = sorted(df['production_companies_name'].dropna().unique())
        prod_selected = st.multiselect("Pays de production", prod_choices[:50])
    with col6:
        st.markdown("**OU**")

    if prod_selected:
        df_prod = df[df['production_companies_name'].isin(prod_selected)]
        films_prod = df_prod.head(10)
        cols = st.columns(10)
        for i, (_, row) in enumerate(films_prod.iterrows()):
            with cols[i]:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=100)
                st.markdown(f"**{row['originalTitle']}**")
                st.caption(f"{row['production_companies_name']} | {row['startYear']}")

    # Section 4 - Recherche par noms et métiers
    st.subheader("🎭 Recherche par noms et métiers")
    col7, col8 = st.columns(2)
    with col7:
        nom_recherche = st.text_input("Nom (acteur, actrice ou réalisateur)")
    with col8:
        job_tri = st.selectbox("Trier par", ["Alphabétique", "Métier"])

    if nom_recherche:
        df_people = df[df['noms'].str.lower().str.contains(nom_recherche.lower(), na=False)]
        if job_tri == "Alphabétique":
            df_people = df_people.sort_values(by="noms")
        else:
            df_people = df_people.sort_values(by="jobs")

        films_people = df_people.head(10)
        cols = st.columns(10)
        for i, (_, row) in enumerate(films_people.iterrows()):
            with cols[i]:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=100)
                st.markdown(f"**{row['originalTitle']}**")
                st.caption(f"{row['jobs']} : {row['noms']} | {row['startYear']}")

# import streamlit as st
# import pandas as pd

# def espace_decouverte():
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

#     # Derniers films par date
#     st.subheader("🎬 Derniers films par date")
#     tri_date = st.selectbox("Trier par année", ["Plus récent", "Plus ancien"])
#     df_sorted_date = df.sort_values(by="startYear", ascending=(tri_date == "Plus ancien"))
#     cols = st.columns(6)
#     for i, (_, row) in enumerate(df_sorted_date.head(12).iterrows()):
#         with cols[i % 6]:
#             if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
#                 st.image(row['url_complet'], width=150)
#             st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
#             st.markdown(f"Genres : {row['genres']}")

#     # Meilleurs films par note
#     st.subheader("⭐ Meilleurs films par note")
#     tri_rating = st.selectbox("Trier par note", ["Note décroissante", "Note croissante"])
#     df_rating = df[df['averageRating'].notna()].copy()
#     df_rating = df_rating.sort_values(by="averageRating", ascending=(tri_rating == "Note croissante"))
#     cols = st.columns(6)
#     for i, (_, row) in enumerate(df_rating.head(12).iterrows()):
#         with cols[i % 6]:
#             if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
#                 st.image(row['url_complet'], width=150)
#             st.markdown(f"**{row['originalTitle']}**")
#             st.write(f"Note : {row['averageRating']}")
#             st.write(f"Année : {row['startYear']}")

#     # Films par société de production
#     st.subheader("🏢 Films par société de production")
#     production_filter = st.selectbox("Rechercher par société de production", sorted(df['production_companies_name'].dropna().unique()))
#     df_prod = df[df['production_companies_name'] == production_filter]
#     cols = st.columns(5)
#     for i, (_, row) in enumerate(df_prod.head(10).iterrows()):
#         with cols[i % 5]:
#             if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
#                 st.image(row['url_complet'], width=150)
#             st.markdown(f"**{row['originalTitle']}**")
#             st.write(f"Année : {row['startYear']}")
#             st.write(f"Genres : {row['genres']}")

#     # Recherche d'acteurs/actrices ou réalisateurs
#     st.subheader("🎭 Recherche par nom ou métier")
#     col5, col6 = st.columns(2)
#     with col5:
#         nom_recherche = st.text_input("Nom de l'acteur ou actrice")
#     with col6:
#         tri_nom = st.radio("Trier par", ["Alphabétique", "Métier"])

#     if nom_recherche:
#         df_people = df[df['noms'].str.lower().str.contains(nom_recherche.lower(), na=False)]
#         if tri_nom == "Alphabétique":
#             df_people = df_people.sort_values(by="noms")
#         else:
#             df_people = df_people.sort_values(by="jobs")

#         cols = st.columns(5)
#         for i, (_, row) in enumerate(df_people.head(10).iterrows()):
#             with cols[i % 5]:
#                 if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
#                     st.image(row['url_complet'], width=150)
#                 st.markdown(f"**{row['originalTitle']}**")
#                 st.write(f"{row['jobs']} : {row['noms']}")
#                 st.write(f"Année : {row['startYear']}")

df = load_data()

st.title("Espace Découverte de Films")

# Derniers films par date
st.subheader("🎬 Derniers films par date")
tri_date = st.selectbox("Trier par année", ["Plus récent", "Plus ancien"])
df_sorted_date = df.sort_values(by="startYear", ascending=(tri_date == "Plus ancien"))

# Affichage des 10 films sur la même ligne
film_ligne = df_sorted_date.head(10)
cols = st.columns(10)
for i, (_, row) in enumerate(film_ligne.iterrows()):
    with cols[i]:
        if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
            st.image(row['url_complet'], width=100)
        st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
        st.markdown(f"Genres : {row['genres']}")

# Meilleurs films par note
st.subheader("⭐ Meilleurs films par note")
tri_rating = st.selectbox("Trier par note", ["Note décroissante", "Note croissante"])
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

# Films par société de production
st.subheader("🏢 Films par société de production")
production_filter = st.selectbox("Rechercher par société de production", sorted(df['production_companies_name'].dropna().unique()))
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

# Recherche d'acteurs/actrices ou réalisateurs
st.subheader("🎭 Recherche par nom ou métier")
col5, col6 = st.columns(2)
with col5:
    nom_recherche = st.text_input("Nom de l'acteur ou actrice")
with col6:
    tri_nom = st.radio("Trier par", ["Alphabétique", "Métier"])

if nom_recherche:
    df_people = df[df['noms'].str.lower().str.contains(nom_recherche.lower(), na=False)]
    if tri_nom == "Alphabétique":
        df_people = df_people.sort_values(by="noms")
    else:
        df_people = df_people.sort_values(by="jobs")

    film_ligne = df_people.head(10)
    cols = st.columns(10)
    for i, (_, row) in enumerate(film_ligne.iterrows()):
        with cols[i]:
            if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                st.image(row['url_complet'], width=100)
            st.markdown(f"**{row['originalTitle']}**")
            st.write(f"{row['jobs']} : {row['noms']}")
            st.write(f"Année : {row['startYear']}")




#espace decouverte

def espace_decouverte():
    df = load_data()
    st.title("Espace Découverte de Films")

    # Derniers films par date
    st.subheader("🎬 Derniers films par date")
    col1, col2 = st.columns([3, 1])
    with col1:
        tri_date = st.selectbox("Trier par année", ["Plus récent", "Plus ancien"])
        df_sorted_date = df.sort_values(by="startYear", ascending=(tri_date == "Plus ancien"))
        for _, row in df_sorted_date.head(12).iterrows():
            r1, r2 = st.columns([1, 3])
            with r1:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=150)
                else:
                    st.text("[Aucune affiche]")
            with r2:
                st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
                st.markdown(f"Genres : {row['genres']}")
    with col2:
        st.write("")

    # Meilleurs films par note
    st.subheader("⭐ Meilleurs films par note")
    col3, col4 = st.columns([3, 1])
    with col3:
        tri_rating = st.selectbox("Trier par note", ["Note décroissante", "Note croissante"])
        df_rating = df[df['averageRating'].notna()].copy()
        df_rating = df_rating.sort_values(by="averageRating", ascending=(tri_rating == "Note croissante"))
        for _, row in df_rating.head(12).iterrows():
            r1, r2 = st.columns([1, 3])
            with r1:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=150)
                else:
                    st.text("[Aucune affiche]")
            with r2:
                st.markdown(f"**{row['originalTitle']}**")
                st.write(f"Note : {row['averageRating']}")
                st.write(f"Année : {row['startYear']}")

    # Films par société de production
    st.subheader("🏢 Films par société de production")
    production_filter = st.selectbox("Rechercher par société de production", sorted(df['production_companies_name'].dropna().unique()))
    df_prod = df[df['production_companies_name'] == production_filter]
    for _, row in df_prod.head(10).iterrows():
        r1, r2 = st.columns([1, 3])
        with r1:
            if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                st.image(row['url_complet'], width=150)
            else:
                st.text("[Aucune affiche]")
        with r2:
            st.markdown(f"**{row['originalTitle']}**")
            st.write(f"Année : {row['startYear']}")
            st.write(f"Genres : {row['genres']}")

    # Recherche d'acteurs/actrices ou réalisateurs
    st.subheader("🎭 Recherche par nom ou métier")
    col5, col6 = st.columns(2)
    with col5:
        nom_recherche = st.text_input("Nom de l'acteur ou actrice")
    with col6:
        tri_nom = st.radio("Trier par", ["Alphabétique", "Métier"])

    if nom_recherche:
        df_people = df[df['noms'].str.lower().str.contains(nom_recherche.lower(), na=False)]
        if tri_nom == "Alphabétique":
            df_people = df_people.sort_values(by="noms")
        else:
            df_people = df_people.sort_values(by="jobs")

        for _, row in df_people.head(10).iterrows():
            r1, r2 = st.columns([1, 3])
            with r1:
                if pd.notna(row['url_complet']) and row['url_complet'].startswith("http"):
                    st.image(row['url_complet'], width=150)
                else:
                    st.text("[Aucune affiche]")
            with r2:
                st.markdown(f"**{row['originalTitle']}**")
                st.write(f"{row['jobs']} : {row['noms']}")
                st.write(f"Année : {row['startYear']}")


##version 3

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

    df = load_data()
    st.header(" 🎬 CINE PROJECT")
    # Initialisation session state
    if "titre_input" not in st.session_state:
        st.session_state.titre_input = ""
    if "genre_selectionne" not in st.session_state:
        st.session_state.genre_selectionne = ""
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    # Titre de l'application
    st.title("Recherche de Films")

    # Barre de recherche + Réinitialisation côte à côte
    col1, col2 = st.columns([3, 1])
    with col1:
        titre_input = st.text_input("Titre du film", value=st.session_state.titre_input)
    with col2:
        if st.button("Réinitialiser le filtre"):
            st.session_state.titre_input = ""
            st.session_state.genre_selectionne = ""
            st.session_state.page_num = 0
            st.rerun()

    # Sélection du genre
    genres_disponibles = sorted(df['genres'].dropna().unique())
    genre_selectionne = st.selectbox(
        "Choisir un genre",
        [""] + genres_disponibles,
        index=([""] + genres_disponibles).index(st.session_state.genre_selectionne)
        if st.session_state.genre_selectionne in genres_disponibles else 0
    )

    # Bouton de recherche
    if st.button("Rechercher"):
        st.session_state.titre_input = titre_input
        st.session_state.genre_selectionne = genre_selectionne
        st.session_state.page_num = 0
        st.rerun()

    # Filtrage
    df_filtre = df.copy()
    if st.session_state.titre_input:
        recherche = st.session_state.titre_input.lower()
        df_filtre = df_filtre[df_filtre["originalTitle"].str.lower().str.contains(recherche)]
    if st.session_state.genre_selectionne:
        df_filtre = df_filtre[df_filtre["genres"] == st.session_state.genre_selectionne]

    df_filtre = df_filtre.sort_values(by="startYear", ascending=False)

# Supprimer les films sans image
    df_filtre = df_filtre[df_filtre["url_complet"].notna() & (df_filtre["url_complet"].str.strip() != "")]

    # Pagination
    page_size = 20
    total_results = len(df_filtre)
    total_pages = (total_results + page_size - 1) // page_size
    page_num = st.session_state.page_num

    start = page_num * page_size
    end = start + page_size
    page_data = df_filtre.iloc[start:end]

    # Affichage des films
    for _, row in page_data.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                poster = row.get("url_complet", "")
                if poster.strip():
                    st.image(poster, width=150)
                else:
                    st.warning("🖼️ Image non disponible.")
            with col2:
                st.subheader(row.get("originalTitle", "Titre inconnu"))
                st.markdown(f"**Genre :** {row.get('genres', 'Non spécifié')}")
                st.markdown(f"**Description :** {row.get('overview', 'Aucune description')}")

    # Navigation
    st.write(f"Page {page_num + 1} sur {total_pages}")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if page_num > 0 and st.button("⬅️ Page précédente"):
            st.session_state.page_num -= 1
            st.rerun()
    with col_next:
        if page_num < total_pages - 1 and st.button("➡️ Page suivante"):
            st.session_state.page_num += 1
            st.rerun()









#version 2
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
from pages import accueil, recherche

# Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche", "Nos recommandations"],
        icons=["film", "search", "stars"],
        menu_icon="camera-reels",
        default_index=0
         )
if selection == "Accueil":
   accueil()

elif selection == "Recherche":
    recherche()

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




#version 1

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

def recherche():
    # Initialisation de la session_state
    if "titre_input" not in st.session_state:
        st.session_state.titre_input = ""
    if "genre_selectionne" not in st.session_state:
        st.session_state.genre_selectionne = ""
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    st.header("🎬 CINE PROJECT")
    st.title("🔍 Recherche de films")

    # Chargement de la base
    df_sans_vec = st.session_state.get("df_sans_vec", None)
    if df_sans_vec is None:
        st.error("❌ Aucune base de données chargée.")
        return

    # Widgets de recherche
    titre_input = st.text_input("Rechercher par titre :", value=st.session_state.titre_input, key="titre_input")
    genre_input = st.selectbox("Rechercher par genre :", [""] + sorted(df_sans_vec["genres"].dropna().unique()), index=0, key="genre_selectionne")

    # Boutons de réinitialisation
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("❌ Réinitialiser le titre"):
            st.session_state.titre_input = ""
            st.session_state.page_num = 0
            st.rerun()
    with col2:
        if st.button("❌ Réinitialiser le genre"):
            st.session_state.genre_selectionne = ""
            st.session_state.page_num = 0
            st.rerun()
    with col3:
        if st.button("🔄 Réinitialiser tous les filtres"):
            st.session_state.titre_input = ""
            st.session_state.genre_selectionne = ""
            st.session_state.page_num = 0
            st.rerun()

    # Filtrage
    df_filtre = df_sans_vec.copy()

    if st.session_state.titre_input:
        df_filtre = df_filtre[df_filtre["originalTitle"].str.contains(st.session_state.titre_input, case=False, na=False)]

    if st.session_state.genre_selectionne:
        df_filtre = df_filtre[df_filtre["genres"].str.contains(st.session_state.genre_selectionne, case=False, na=False)]

    # Supprimer les films sans image
    df_filtre = df_filtre[df_filtre["url_complet"].notna() & (df_filtre["url_complet"].str.strip() != "")]

    # Pagination
    page_size = 20
    total_results = len(df_filtre)
    total_pages = (total_results + page_size - 1) // page_size
    page_num = st.session_state.page_num

    start = page_num * page_size
    end = start + page_size
    page_data = df_filtre.iloc[start:end]

    # Affichage des films
    for _, row in page_data.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                poster = row.get("url_complet", "")
                if poster.strip():
                    st.image(poster, width=150)
                else:
                    st.warning("🖼️ Image non disponible.")
            with col2:
                st.subheader(row.get("originalTitle", "Titre inconnu"))
                st.markdown(f"**Genre :** {row.get('genres', 'Non spécifié')}")
                st.markdown(f"**Description :** {row.get('overview', 'Aucune description')}")

    # Navigation
    st.write(f"Page {page_num + 1} sur {total_pages}")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if page_num > 0 and st.button("⬅️ Page précédente"):
            st.session_state.page_num -= 1
            st.rerun()
    with col_next:
        if page_num < total_pages - 1 and st.button("➡️ Page suivante"):
            st.session_state.page_num += 1
            st.rerun()









# def recherche():
#     st.header("🎬 CINE PROJECT")
#     st.title("🔍 Recherche de films")

#     df_sans_vec = st.session_state.get("df_sans_vec", None)
#     if df_sans_vec is None:
#         st.error("❌ Aucune base de données chargée.")
#         return

# #     # Filtrer uniquement les films avec une image
# #     df_sans_vec = df_sans_vec[
# #     df_sans_vec["url_complet"].notna() &
# #     df_sans_vec["url_complet"].str.strip().ne("") &
# #     df_sans_vec["url_complet"].str.lower().str.match(r".*\.(jpg|jpeg|png|gif|webp)$")
# # ]



#     # # --- Initialisation session_state ---
#     # if "page_num" not in st.session_state:
#     #     st.session_state.page_num = 0
#     # if "reset_trigger" not in st.session_state:
#     #     st.session_state.reset_trigger = False

#     # # --- Interface de recherche ---
#     # genres = sorted(df_sans_vec["genres"].dropna().str.split(',').explode().unique())

#     # if st.session_state.reset_trigger:
#     #     titre_input = ""
#     #     genre_selectionne = ""
#     #     st.session_state.reset_trigger = False  # Reset le trigger
#     # else:
#     #     titre_input = st.session_state.get("titre_input", "")
#     #     genre_selectionne = st.session_state.get("genre_selectionne", "")

#     # # Champs de recherche
#     # titre_input = st.text_input("🎬 Rechercher un titre :", value=titre_input)
#     # genre_selectionne = st.selectbox("📚 Filtrer par genre :", options=[""] + genres, index=(genres.index(genre_selectionne)+1) if genre_selectionne in genres else 0)

#     # # Mémoriser les valeurs dans session_state
#     # st.session_state["titre_input"] = titre_input
#     # st.session_state["genre_selectionne"] = genre_selectionne



# # Initialiser les valeurs si elles n'existent pas
#     if "titre_input" not in st.session_state:
#         st.session_state["titre_input"] = ""
#     if "genre_selectionne" not in st.session_state:
#         st.session_state["genre_selectionne"] = ""

#     # Champs de recherche
#     titre_input = st.text_input("🎬 Rechercher un titre :", st.session_state["titre_input"], key="titre_input_widget")
#     genre_selectionne = st.selectbox("📚 Filtrer par genre :", ["", "Action", "Comédie", "Drame"], index=0 if st.session_state["genre_selectionne"] == "" else ["", "Action", "Comédie", "Drame"].index(st.session_state["genre_selectionne"]), key="genre_widget")

#     # Mise à jour des valeurs
#     st.session_state["titre_input"] = titre_input
#     st.session_state["genre_selectionne"] = genre_selectionne

#     # Boutons de réinitialisation
#     col1, col2, col3 = st.columns([1, 1, 2])
#     with col1:
#         if st.button("❌ Réinitialiser le titre"):
#             st.session_state["titre_input"] = ""
#             st.rerun()

#     with col2:
#         if st.button("❌ Réinitialiser le genre"):
#             st.session_state["genre_selectionne"] = ""
#             st.rerun()

#     with col3:
#         if st.button("🔄 Réinitialiser tous les filtres"):
#             st.session_state["titre_input"] = ""
#             st.session_state["genre_selectionne"] = ""
#             st.rerun()








#     # # Boutons de réinitialisation SOUS les champs
#     # col1, col2, col3 = st.columns([1, 1, 2])
#     # with col1:
#     #     if st.button("❌ Réinitialiser le titre"):
#     #         st.session_state["titre_input"] = ""
#     #         st.session_state.page_num = 0
#     #         st.rerun()
#     # with col2:
#     #     if st.button("❌ Réinitialiser le genre"):
#     #         st.session_state["genre_selectionne"] = ""
#     #         st.session_state.page_num = 0
#     #         st.rerun()
#     # with col3:
#     #     if st.button("🔄 Réinitialiser tous les filtres"):
#     #         st.session_state.reset_trigger = True
#     #         st.session_state.page_num = 0
#     #         st.rerun()

# # # --- Boutons de réinitialisation ---
# #     col1, col2, col3 = st.columns([1, 1, 2])
# #     with col1:
# #         if st.button("❌ Réinitialiser le titre"):
# #             st.session_state.pop("titre_input", None)
# #             st.session_state["page_num"] = 0
# #             st.rerun()

# #     with col2:
# #         if st.button("❌ Réinitialiser le genre"):
# #             st.session_state.pop("genre_selectionne", None)
# #             st.session_state["page_num"] = 0
# #             st.rerun()

# #     with col3:
# #         if st.button("🔄 Réinitialiser tous les filtres"):
# #             st.session_state.pop("titre_input", None)
# #             st.session_state.pop("genre_selectionne", None)
# #             st.session_state["page_num"] = 0
# #             st.rerun()




# # # Boutons de réinitialisation sous les champs
# #     col1, col2, col3 = st.columns([1, 1, 2])
# #     with col1:
# #         if st.button("❌ Réinitialiser le titre"):
# #             st.session_state.titre_input = ""
# #             st.rerun()

# #     with col2:
# #         if st.button("❌ Réinitialiser le genre"):
# #             st.session_state.genre_selectionne = ""
# #             st.rerun()

# #     with col3:
# #         if st.button("🔄 Réinitialiser tous les filtres"):
# #             st.session_state.reset = True
# #             st.rerun()


#     # --- Application des filtres ---
#     df_filtre = df_sans_vec.copy()

#     if titre_input:
#         df_filtre = df_filtre[df_filtre["originalTitle"].str.contains(titre_input, case=False, na=False)]

#     if genre_selectionne:
#         df_filtre = df_filtre[df_filtre["genres"].str.contains(genre_selectionne, na=False)]

#     df_filtre = df_filtre.sort_values(by="startYear", ascending=False)

#     if df_filtre.empty:
#         st.warning("❌ Aucun résultat. Essayez de modifier ou retirer un filtre.")
#         return

#     # --- Pagination ---
#     page_size = 10
#     start = st.session_state.page_num * page_size
#     end = start + page_size
#     page_df = df_filtre.iloc[start:end]

#     st.markdown("### 🎞️ Résultats :")
#     for idx, row in page_df.iterrows():
#         col1, col2 = st.columns([1, 5])
#         with col1:
#             st.image(row["url_complet"], width=80)
#         with col2:
#             if st.button(f"{row['originalTitle']} ({row['startYear']})", key=f"film_{idx}"):
#                 st.session_state["film_selectionne"] = row.to_dict()
#                 st.session_state["page"] = "details"
#                 st.rerun()

#     # --- Navigation pagination ---
#     total_pages = len(df_filtre) // page_size + int(len(df_filtre) % page_size > 0)
#     nav1, nav2, nav3 = st.columns([1, 2, 1])
#     with nav1:
#         if st.session_state.page_num > 0:
#             if st.button("⬅️ Page précédente"):
#                 st.session_state.page_num -= 1
#                 st.rerun()
#     with nav2:
#         st.markdown(f"<div style='text-align:center'>Page {st.session_state.page_num + 1} / {total_pages}</div>", unsafe_allow_html=True)
#     with nav3:
#         if end < len(df_filtre):
#             if st.button("➡️ Page suivante"):
#                 st.session_state.page_num += 1
#                 st.rerun()

