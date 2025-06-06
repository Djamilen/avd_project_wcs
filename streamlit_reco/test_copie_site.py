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