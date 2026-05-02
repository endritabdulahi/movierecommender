from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_content_recommendations(movies, movie_title, top_n=10):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(movies["genres"])

    similarity_matrix = cosine_similarity(tfidf_matrix)

    idx = movies[movies["title"] == movie_title].index[0]

    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    indices = [i[0] for i in scores]

    return movies.iloc[indices][["title", "genres"]].reset_index(drop=True)