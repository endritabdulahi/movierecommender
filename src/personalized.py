import pandas as pd
from hybrid import get_hybrid_recommendations


def get_personalized_recommendations(movie_ratings, movies, profile_ratings, top_n=10):
    all_recommendations = []

    for movie_title, user_rating in profile_ratings.items():
        if user_rating < 4:
            continue

        recs = get_hybrid_recommendations(movie_ratings, movies, movie_title)
        recs = recs.copy()

        recs["user_weight"] = user_rating
        recs["personalized_score"] = recs["final_score"] * user_rating

        all_recommendations.append(recs)

    if not all_recommendations:
        return pd.DataFrame()

    combined = pd.concat(all_recommendations)

    # Do not recommend movies the user already rated
    rated_movies = list(profile_ratings.keys())
    combined = combined[~combined["title"].isin(rated_movies)]

    combined = combined.groupby("title").agg(
        personalized_score=("personalized_score", "mean"),
        final_score=("final_score", "mean"),
        num_ratings=("num_ratings", "max")
    ).reset_index()

    combined = combined.sort_values("personalized_score", ascending=False)

    return combined.head(top_n)