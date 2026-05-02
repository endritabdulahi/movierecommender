# "Movie Recommendation System"

A hybrid movie recommender system that suggests movies based on user preferences, ratings, and content similarity.

---

## *Features*

-  Fuzzy Search (handles typos like "batmn" → Batman)
-  Hybrid Recommendation System
  - Collaborative Filtering (user ratings)
  - Content-Based Filtering (genres)
-  User Profiles
  - Create and load profiles
  - Rate movies (1–5 stars)
-  Personalized Recommendations
  - Based on user’s highly rated movies
-  Movie Posters
  - Fetched using TMDB API
-  Fast Performance (caching)
-  Interactive UI (Streamlit)

---

#  *How It Works*

### 1. Collaborative Filtering
Finds movies liked by users with similar rating patterns.

### 2. Content-Based Filtering
Recommends movies with similar genres.

### 3. Hybrid Model

Combines both approaches:

final_score = 0.7 * rating_score + 0.3 * content_score

### 4. Personalization
- Uses user ratings (4–5 stars)
- Combines recommendations from favorite movies
- Removes already rated movies

---

##  *Example*

Search:

*batmn*

App suggests:

*Batman (1989)*
*Batman Returns (1992)*

Displays:
- Posters
- Scores
- Genres

---

##  Tech Stack

- Python
- Pandas
- Scikit-learn
- Streamlit
- RapidFuzz
- TMDB API

---

##  Installation

### 1. Clone the repo

git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender

### 2. Create virtual environment

-m venv .venv
.venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

---

##  Setup API Key

1. Go to: https://www.themoviedb.org/
2. Create account
3. Get API key
4. Add to `app.py`:

API_KEY = "your_api_key_here"

---

## Run the App

python -m streamlit run app.py

---

##  User Profiles

- Create a profile in sidebar
- Rate movies
- Click "Recommend Based on My Ratings"
- Get personalized results

---

## 📁 Project Structure

src/
├── app.py
├── main.py
├── hybrid.py
├── personalized.py
├── profiles.py
├── data_loader.py
├── similarity.py
├── content_based.py
└── profiles.json

---

##  Future Improvements

- Deploy online
- Improve model (SVD / matrix factorization)
- Add genre filters
- Add authentication
- Improve UI

---

##  Acknowledgements

- MovieLens dataset
- TMDB API
- Streamlit

---

## 📬 Author

Endrit Abdulahi
