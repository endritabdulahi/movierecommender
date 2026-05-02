import pandas as pd
from similarity import get_similar_movies
from content_based import get_content_recommendations

def get_hybrid_recommendations(movie_ratings, movies, movie_title):
    
    collab = get_similar_movies(movie_ratings, movie_title)
    content = get_content_recommendations(movies, movie_title)

    collab = collab.reset_index()
    collab.columns = ["title", "rating_score", "num_ratings"]

    content = content.copy()
    content["content_score"] = 1

    hybrid = pd.merge(collab, content, on="title", how="outer")

    hybrid["rating_score"] = hybrid["rating_score"].fillna(0)
    hybrid["content_score"] = hybrid["content_score"].fillna(0)

    hybrid["rating_score"] = hybrid["rating_score"].fillna(0)

    hybrid["num_ratings"] = hybrid["num_ratings"].fillna(0)
    hybrid["weighted_score"] = hybrid["rating_score"] * (hybrid["num_ratings"] / (hybrid["num_ratings"] + 50))

    hybrid["final_score"] = 0.6 * hybrid["weighted_score"] + 0.4 * hybrid["content_score"]

    hybrid = hybrid[hybrid["title"] != movie_title]

    return hybrid.sort_values("final_score", ascending=False)