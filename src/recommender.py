def get_popular_movies(movie_ratings, min_ratings=50, top_n=10):
    movie_stats = movie_ratings.groupby("title").agg(
        average_rating=("rating", "mean"),
        number_of_ratings=("rating", "count")
    )

    popular_movies = movie_stats[movie_stats["number_of_ratings"] >= min_ratings]

    popular_movies = popular_movies.sort_values(
        by="average_rating",
        ascending=False
    )

    return popular_movies.head(top_n)