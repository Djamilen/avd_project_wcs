import streamlit as st
import pandas as pd
import plotly.express as px
from utils import is_valid_image
from yt_dlp import YoutubeDL


def session_states():
    st.session_state.setdefault("query", "")
    st.session_state.setdefault("last_query", "")
    st.session_state.setdefault("page_num", 0)
    st.session_state.setdefault("film_selectionne", None)
    st.session_state.setdefault("page", "Accueil")
    st.session_state.setdefault("reset", False)
   

def scrap_video(movie_title):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True
    }
    query = f"ytsearch1:{movie_title} bande annonce"
    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(query, download=False)
            return result["entries"][0]["url"]
        except:
            return None

def reco():
    df = st.session_state["df_final_translated"]

    if st.session_state.film_selectionne is None:
        st.warning("Aucun film sélectionné.")
        return

    st.write(f"Film sélectionné : {st.session_state.film_selectionne}")
    film = df.loc[st.session_state.film_selectionne]

    col1, col2 = st.columns([1, 2])
    with col1:
        image_url = film['url_complet']
        if is_valid_image(image_url):
            st.image(image_url, width=300)
        else:
            st.image("image/Pas_d_image.png", width=300)

        video_url = scrap_video(film['originalTitle'])
        if video_url:
            st.video(video_url)
        else:
            st.info("Pas de bande-annonce disponible.")

    with col2:
        st.title(film['originalTitle'])
        st.subheader(f"Année : {film['startYear']}")

        # 🎬 Réalisateur avec hiérarchie : d'abord noms/category, sinon primaryName
        try:
            noms = eval(film.get("noms", "[]"))
            roles = eval(film.get("jobs", "[]"))
            realisateurs_identifies = [nom for nom, role in zip(noms, roles) if (role == "director" or role == "real")]

            if realisateurs_identifies:
                st.write(f"🎬 Réalisateur : {', '.join(realisateurs_identifies)}")
            else:
                primary_name = film.get("primaryName")
                if primary_name and isinstance(primary_name, str):
                    st.write(f"🎬 Réalisateur : {primary_name} (non vérifié)")
                else:
                    st.write("🎬 Réalisateur : Non disponible")
        except Exception as e:
            st.write("🎬 Réalisateur : Non disponible")
            print(f"Erreur réalisateur : {e}")

        # 🎭 Acteurs principaux
        try:
            acteurs = eval(film.get("noms", "[]"))
            premiers = acteurs[:10]
            restants = acteurs[10:]

            st.write(f"🎭 Acteurs principaux : {', '.join(premiers)}")

            if restants:
                with st.expander("Voir plus d’acteurs"):
                    st.write(", ".join(restants))
        except:
            st.write("🎭 Acteurs : Non disponible")

        # 📚 Genres
        st.write(f"📚 Genre(s) : {', '.join(eval(film.get('genres_list', '[]')))}")
        # ⏱️ Durée
        st.write(f"⏱️ Durée : {film.get('runtimeMinutes', 'Non renseignée')} min")

        # Résumé
        st.markdown("---")
        st.subheader("Résumé")
        st.write(film.get("overview_fr", "Aucun résumé disponible."))
        st.markdown("---")

    # Chargement des recommandations
    reco_df = st.session_state["df_reco_film"]
    st.subheader("🎯 Films recommandés")

    raw_recos_str = reco_df.loc[film.name]["recos"]
    rec_titles = eval(raw_recos_str)[:10]
    #st.write(rec_titles)

    reco_films = df.loc[rec_titles]

    if "reco_page" not in st.session_state:
        st.session_state.reco_page = 0

    start = st.session_state.reco_page * 5
    end = start + 5
    for i, (_, rec_film) in enumerate(reco_films.iloc[start:end].iterrows()):
        cols = st.columns([1, 4])
        with cols[0]:
            st.image(rec_film["url_complet"], width=100)
        with cols[1]:
            st.markdown(f"**{rec_film['originalTitle']}** ({rec_film['startYear']})")
            st.write(", ".join(eval(rec_film.get('genres', '[]'))))
            if st.button("Accéder", key=f"reco_{start+i}"):
                st.session_state["film_selectionne"] = rec_film.name
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                print(st.session_state["film_selectionne"] )
                st.session_state.reco_page = 0
                st.rerun()

    col_left, col_right = st.columns([1, 1])
    with col_left:
        if st.session_state.reco_page > 0:
            if st.button("⬅️ Revenir aux précédents"):
                st.session_state.reco_page -= 1
                st.rerun()
    with col_right:
        if end < len(reco_films):
            if st.button("Voir plus ➡️"):
                st.session_state.reco_page += 1
                st.rerun()
                
# 🔙 Bouton retour à la recherche
st.markdown("---")
if st.button("🔙 Retour à la recherche"):
    st.session_state["page"] = "recherche"
    st.session_state["film_selectionne"] = None
    st.session_state["reco_page"] = 0
    st.rerun()