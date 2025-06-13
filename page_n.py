import streamlit as st
import pandas as pd
import plotly.express as px
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
    df = st.session_state["csv/df_final"]
    session_states()

    # Saisie de recherche
    query = st.text_input("Tape un titre ou un nom", value=st.session_state.query, placeholder="🔎 Réveille toi, il faut effectuer un recherche ;) ...")

    # Boutons Entrer / Réinitialiser
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Entrer"):
            st.session_state.query = query
            st.session_state.page_num = 0
    with col2:
        if st.button("Réinitialiser"):
            st.session_state.query = ""
            st.session_state.page_num = 0
            st.rerun()

    # Recherche si une requête est enregistrée
    if st.session_state.query:
        filtres = df[
            df['originalTitle'].str.lower().str.contains(st.session_state.query.lower(), na=False) |
            df['primaryName'].str.lower().str.contains(st.session_state.query.lower(), na=False)
        ]

        page = st.session_state.page_num
        start, end = page * 9, (page + 1) * 9
        for i in range(start, min(end, len(filtres)), 3):
            cols = st.columns(3)
            for j, (_, row) in enumerate(filtres.iloc[i:i+3].iterrows()):
                with cols[j]:
                    st.image(row['url_complet'], width=300)
                    st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
                    st.write(row['genres'])
                    if st.button("Accéder", key=f"btn_{i}_{j}"):
                        st.session_state["film_selectionne"] = row.name
                        st.session_state["page"] = "Reco"
                        st.rerun()

        total_pages = (len(filtres) - 1) // 9 + 1
        st.markdown(f"Page {page+1} / {total_pages}")

        col_g, col_d = st.columns([1, 1])
        with col_g:
            if page > 0 and st.button("⬅️ Page précédente"):
                st.session_state.page_num -= 1
                st.rerun()
        with col_d:
            if end < len(filtres) and st.button("➡️ Page suivante"):
                st.session_state.page_num += 1
                st.rerun()

    

def espace_decouverte():
    pass

def reco():
    df = st.session_state["csv/df_final"]
    session_states()

    if st.session_state.film_selectionne is None:
        st.warning("Aucun film sélectionné.")
        return

    film = df.loc[st.session_state.film_selectionne]

    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        
        st.image(film['url_complet'], width=300)
        # ✅ Ajout de la vidéo réduite sous l’affiche
        video_url = scrap_video(film['originalTitle'])
        if video_url:
            st.video(video_url)
        else:
            st.info("Pas de bande-annonce disponible.")
            
    with col2:
        st.title(film['originalTitle'])
        st.subheader(f"Année : {film['startYear']}")
        st.write(f"🎬 Réalisateur : {', '.join(eval(film.get('primaryName', '[]')))}")
        st.write(f"🎭 Acteurs : {', '.join(eval(film.get('noms', '[]')))}")
        st.write(f"📚 Genre(s) : {', '.join(eval(film.get('genres', '[]')))}")
        st.write(f"⏱️ Durée : {film.get('runtimeMinutes', 'Non renseignée')} min")

        st.markdown("---")
        st.subheader("Résumé")
        st.write(film.get("overview", "Aucun résumé disponible."))


    

    
