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


def accueil():
    st.title("🎬 CINE PROJECT")
    st.markdown(
        """
        Bienvenue sur CINE PROJECT, votre destination pour découvrir et explorer l'univers du cinéma.  
        Notre ADN repose sur la passion du 7ème art, le partage d'idées et l'inspiration.  
        Des recommandations qui vous correspondent grâce à une analyse ciblée du marché du cinéma français.  
        Des données mises à jour en temps réel en fonction des dernières sorties et avis du public,  
        exclusivement orientées selon les attentes des spectateurs français.
        """
    )

    df1 = pd.DataFrame({
        'Année': list(range(2015, 2025)),
        'Films français': [90, 95, 97, 92, 89, 25, 35, 50, 65, 55],
        'Films américains': [110, 115, 100, 90, 115, 20, 30, 40, 50, 45],
        'Films européens': [20, 22, 25, 28, 20, 8, 12, 18, 20, 25]
    })

    df2 = pd.DataFrame({
        'Année': list(range(2007, 2025)),
        'Entrées (millions)': [178, 190, 201, 207, 217, 203, 193, 209, 205, 213,
                              209, 201, 213, 65, 95, 152, 180, 181]
    })

    df1_melted = df1.melt(id_vars='Année', var_name='Nationalité', value_name='Entrées')
    fig1 = px.line(df1_melted, x='Année', y='Entrées', color='Nationalité',
                   markers=True, title="Entrées en salle par nationalité (2015–2024)", height=400)

    fig2 = px.bar(df2, x='Année', y='Entrées (millions)', text='Entrées (millions)',
                  title="Entrées totales en millions (2007–2024)", height=400)
    fig2.update_traces(textposition='outside')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

def recherche():
    df = st.session_state["df_final_translated"]

    # Suggestions films + personnes
    titres = df['originalTitle'].dropna().unique().tolist()
    noms = df['noms'].dropna().tolist()
    personnes = set()
    for liste in noms:
        try:
            personnes.update(eval(liste))
        except:
            pass
    suggestions = sorted(set(titres) | personnes)

    # Barre de recherche
    query = st.selectbox(
        "🔎 Tape un film ou un nom",
        options=[""] + suggestions,
        index=0,
        placeholder="🔎 Tape un nom de film ou d'acteur pour commencer ta recherche."
    )

    # Boutons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrer"):
            st.session_state.query = query
            st.session_state.page_num = 0
            st.rerun()
    with col2:
        if st.button("Réinitialiser"):
            st.session_state.query = ""
            st.session_state.page_num = 0
            st.rerun()

    if not st.session_state.query:
        return

    q = st.session_state.query.lower()
    filtres = df[
        df['originalTitle'].str.lower().str.contains(q, na=False) |
        df['noms'].str.lower().str.contains(q, na=False) |
        df['primaryTitle'].str.lower().str.contains(q, na=False) 
    ]

    page = st.session_state.page_num
    start, end = page * 9, (page + 1) * 9
    for i in range(start, min(end, len(filtres)), 3):
        cols = st.columns(3)
        for j, (_, row) in enumerate(filtres.iloc[i:i+3].iterrows()):
            with cols[j]:
                image_url = row['url_complet'] 
                if is_valid_image(image_url):
                    st.image(image_url, width=150)
                else:
                    st.image("image/Pas_d_image.png", width=150)

                st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
                #st.write(', '.join(eval(row.get("genres", "[]"))))
                if st.button("Accéder", key=f"btn_{i}_{j}"):
                    st.session_state["film_selectionne"] = row.name
                    st.session_state["page"] = "Reco"
                    st.rerun()

    total_pages = (len(filtres) - 1) // 9 + 1
    st.markdown(f"Page {page+1} / {total_pages}")

    col1, col2 = st.columns(2)
    with col1:
        if page > 0 and st.button("⬅️ Précédente"):
            st.session_state.page_num -= 1
            st.rerun()
    with col2:
        if end < len(filtres) and st.button("➡️ Suivante"):
            st.session_state.page_num += 1
            st.rerun()

    

def espace_decouverte():
    pass

def reco():
    df = st.session_state["df_final_translated"]

    if st.session_state.film_selectionne is None:
        st.warning("Aucun film sélectionné.")
        return

    st.write(f"Film sélectionné : {st.session_state.film_selectionne}")
    film = df.loc[st.session_state.film_selectionne]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(film['url_complet'], width=300)
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
            roles = eval(film.get("category", "[]"))
            realisateurs_identifies = [nom for nom, role in zip(noms, roles) if role == "director"]

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
        st.write(f"📚 Genre(s) : {', '.join(eval(film.get('genres', '[]')))}")
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
    st.write(rec_titles)

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



    

    
