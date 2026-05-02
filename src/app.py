import re
import requests
import streamlit as st
from rapidfuzz import process

from data_loader import load_movie_ratings, load_movies_with_genres
from hybrid import get_hybrid_recommendations
from profiles import load_profiles, add_profile, add_rating
from personalized import get_personalized_recommendations


API_KEY = "INSERT API KEY FROM TMDB or any other website..."


if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "personalized_mode" not in st.session_state:
    st.session_state.personalized_mode = False


def clean_title(title):
    title = re.sub(r"\(\d{4}\)", "", title)

    if ", The" in title:
        title = "The " + title.replace(", The", "")

    if ", A" in title:
        title = "A " + title.replace(", A", "")

    if ", An" in title:
        title = "An " + title.replace(", An", "")

    return title.strip()


def get_poster(movie_title):
    search_title = clean_title(movie_title)

    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": search_title
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except:
        return None

    return None


@st.cache_data
def load_data():
    movie_ratings = load_movie_ratings()
    movies = load_movies_with_genres()
    titles = movie_ratings["title"].unique().tolist()
    return movie_ratings, movies, titles


st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.markdown("### 🍿 Find your next favorite movie")
st.write("Type a movie name or get personalized recommendations from your saved ratings.")


movie_ratings, movies, titles = load_data()


# -------------------------
# User profiles
# -------------------------

st.sidebar.title("👤 User Profiles")

profiles = load_profiles()

profile_name = st.sidebar.text_input("Enter profile name:")

if st.sidebar.button("Create / Load Profile"):
    if profile_name:
        profiles = add_profile(profile_name)
        st.sidebar.success(f"Profile loaded: {profile_name}")

if profiles:
    selected_profile = st.sidebar.selectbox(
        "Select profile:",
        list(profiles.keys())
    )

    st.sidebar.subheader("Saved Ratings")

    if profiles[selected_profile]:
        for movie, rating in profiles[selected_profile].items():
            st.sidebar.write(f"{movie}: ⭐ {rating}")
    else:
        st.sidebar.write("No ratings saved yet.")

    if st.sidebar.button("Recommend Based on My Ratings"):
        st.session_state.personalized_mode = True
        st.session_state.selected_movie = None

else:
    selected_profile = None


# -------------------------
# Movie search
# -------------------------

user_input = st.text_input("Enter a movie name:")

if user_input:
    matches = process.extract(user_input, titles, limit=5)
    match_titles = [match[0] for match in matches]

    selected_movie = st.selectbox(
        "Did you mean:",
        match_titles,
        index=0
    )

    if st.button("Recommend Similar Movies"):
        st.session_state.selected_movie = selected_movie
        st.session_state.personalized_mode = False


# -------------------------
# Personalized recommendations
# -------------------------

if st.session_state.personalized_mode and selected_profile:
    profile_ratings = profiles[selected_profile]

    personalized_recs = get_personalized_recommendations(
        movie_ratings,
        movies,
        profile_ratings
    )

    st.subheader(f"👤 Personalized recommendations for {selected_profile}")

    if personalized_recs.empty:
        st.write("Rate some movies 4 or 5 stars first.")
    else:
        personalized_recs = personalized_recs.merge(
            movies[["title", "genres"]],
            on="title",
            how="left"
        )

        personalized_recs["genres"] = personalized_recs["genres"].fillna("Unknown")

        cols = st.columns(3)

        for i, row in enumerate(personalized_recs.head(9).itertuples()):
            with cols[i % 3]:
                poster = get_poster(row.title)

                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown("🎬")

                st.markdown(f"### {row.title}")
                st.write(f"⭐ Personalized Score: {row.personalized_score:.2f}")
                st.write(f"👥 Ratings: {row.num_ratings}")
                st.write(f"🎭 {row.genres}")


# -------------------------
# Similar movie recommendations
# -------------------------

if st.session_state.selected_movie:
    recommendations = get_hybrid_recommendations(
        movie_ratings,
        movies,
        st.session_state.selected_movie
    )

    recommendations = recommendations.drop(columns=["genres"], errors="ignore")

    recommendations = recommendations.merge(
        movies[["title", "genres"]],
        on="title",
        how="left"
    )

    recommendations["genres"] = recommendations["genres"].fillna("Unknown")

    st.subheader(f"🎬 Recommendations for: {st.session_state.selected_movie}")

    cols = st.columns(3)

    for i, row in enumerate(recommendations.head(9).itertuples()):
        with cols[i % 3]:
            poster = get_poster(row.title)

            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.markdown("🎬")

            st.markdown(f"### {row.title}")
            st.write(f"⭐ Score: {row.final_score:.2f}")
            st.write(f"👥 Ratings: {row.num_ratings}")
            st.write(f"🎭 {row.genres}")

            if selected_profile:
                rating = st.slider(
                    f"Rate {row.title}",
                    min_value=1,
                    max_value=5,
                    value=profiles[selected_profile].get(row.title, 3),
                    key=f"{selected_profile}_{row.title}"
                )

                if st.button("Save Rating", key=f"save_{selected_profile}_{row.title}"):
                    add_rating(selected_profile, row.title, rating)
                    st.toast("Saved!")
                    st.rerun()