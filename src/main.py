from data_loader import load_movie_ratings, load_movies_with_genres
from hybrid import get_hybrid_recommendations
from rapidfuzz import process

movie_ratings = load_movie_ratings()
movies = load_movies_with_genres()
titles = movie_ratings["title"].unique().tolist()

while True:
    user_input = input("\nEnter a movie name (or 'exit'): ")

    if user_input.lower() == "exit":
        print("Goodbye")
        break

    matches = process.extract(user_input, titles, limit=5)

    print("\nDid you mean:")
    for i, (title, score, _) in enumerate(matches):
        print(f"{i}: {title} (score: {score})")

    try:
        choice = int(input("\nChoose a number: "))
        selected_movie = matches[choice][0]
    except:
        print("Invalid choice, try again.")
        continue

    recommendations = get_hybrid_recommendations(
        movie_ratings,
        movies,
        selected_movie
    )

    print(f"\nRecommendations for: {selected_movie}\n")

    for number, row in enumerate(recommendations.head(10).itertuples(), start=1):
        print(f"{number}. {row.title}  Score: {row.final_score:.2f}")