import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_ratings():
    ratings_path = BASE_DIR / "data" / "ml-100k" / "u.data"

    return pd.read_csv(
        ratings_path,
        sep="\t",
        names=["user_id", "movie_id", "rating", "timestamp"]
    )


def load_movies():
    movies_path = BASE_DIR / "data" / "ml-100k" / "u.item"

    return pd.read_csv(
        movies_path,
        sep="|",
        encoding="latin-1",
        usecols=[0, 1],
        names=["movie_id", "title"]
    )


def load_movie_ratings():
    ratings = load_ratings()
    movies = load_movies()

    return ratings.merge(movies, on="movie_id")

def load_movies_with_genres():
    movies_path = BASE_DIR / "data" / "ml-100k" / "u.item"

    genre_columns = [
        "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]

    columns = [
        "movie_id", "title", "release_date", "video_release_date", "imdb_url"
    ] + genre_columns

    movies = pd.read_csv(
        movies_path,
        sep="|",
        encoding="latin-1",
        names=columns
    )

    movies["genres"] = movies[genre_columns].apply(
        lambda row: " ".join([g for g in genre_columns if row[g] == 1]),
        axis=1
    )

    return movies[["movie_id", "title", "genres"]]