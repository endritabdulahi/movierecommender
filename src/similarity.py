import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def get_similar_movies(movie_ratings, movie_title):
    movie_matrix = movie_ratings.pivot_table(
        index="user_id",
        columns="title",
        values="rating"
    )

    movie_ratings_series = movie_matrix[movie_title]

    similar = movie_matrix.corrwith(movie_ratings_series)

    corr_df = pd.DataFrame(similar, columns=["correlation"])
    corr_df = corr_df.dropna()

    ratings_count = movie_ratings.groupby("title")["rating"].count()
    corr_df["num_ratings"] = ratings_count

    corr_df = corr_df[corr_df["num_ratings"] > 50]

    corr_df = corr_df.drop(movie_title, errors="ignore")

    return corr_df.sort_values("correlation", ascending=False).head(10)