# -*- coding: utf-8 -*-
"""Movie recommendation system.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YBAjP7Ga0jtROVQ0zrn-Q5uXgShKhoDT
"""

!pip install scikit-surprise

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Load the datasets from MovieLens 100K
ratings_url = "https://files.grouplens.org/datasets/movielens/ml-100k/u.data"
movies_url = "https://files.grouplens.org/datasets/movielens/ml-100k/u.item"
columns_ratings = ["user_id", "movie_id", "rating", "timestamp"]
columns_movies = ["movie_id", "title", "release_date", "video_release_date",
                  "IMDb_URL", "unknown", "Action", "Adventure", "Animation",
                  "Children's", "Comedy", "Crime", "Documentary", "Drama",
                  "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
                  "Romance", "Sci-Fi", "Thriller", "War", "Western"]

# Load ratings and movies
ratings = pd.read_csv(ratings_url, sep="\t", names=columns_ratings, encoding="latin-1")
movies = pd.read_csv(movies_url, sep="|", names=columns_movies, encoding="latin-1")

# Merge ratings and movies
data = pd.merge(ratings, movies, on="movie_id")

# Display dataset shapes and first few rows
ratings_shape = ratings.shape
movies_shape = movies.shape
data_head = data.head()

ratings_shape, movies_shape, data_head

data

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split as surprise_train_test_split
from surprise.model_selection import cross_validate

# Normalize ratings and split into train and test sets
user_mean_ratings = data.groupby('user_id')['rating'].transform('mean')
data['normalized_rating'] = data['rating'] - user_mean_ratings

train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Display shapes of the training and testing datasets
train_shape = train_data.shape
test_shape = test_data.shape

train_shape, test_shape

from surprise import SVD
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split as surprise_train_test_split
from surprise.accuracy import rmse

# Prepare data for Surprise library
reader = Reader(rating_scale=(0.5, 5))  # Rating scale from 0.5 to 5
data_surprise = Dataset.load_from_df(data[['user_id', 'movie_id', 'rating']], reader)

# Split data into train and test sets (for Surprise library)
trainset, testset = surprise_train_test_split(data_surprise, test_size=0.2, random_state=42)

# Train the SVD model
svd = SVD()
svd.fit(trainset)

# Evaluate the model
predictions = svd.test(testset)
collab_rmse = rmse(predictions)

print(f"Collaborative Filtering RMSE: {collab_rmse}")

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

# Extract genre features
genre_features = movies.iloc[:, 6:].values
genre_features = normalize(genre_features)

# Compute cosine similarity
genre_similarity = cosine_similarity(genre_features)

# Function to recommend movies based on content
def recommend_content(user_id, top_n=5):
    # Get movies rated by the user
    user_movies = train_data[train_data['user_id'] == user_id]

    # Sort by user's highest ratings
    top_movies = user_movies.sort_values('rating', ascending=False)['movie_id'].values[:5]

    # Find similar movies
    similar_movies = []
    for movie_id in top_movies:
        sim_scores = list(enumerate(genre_similarity[movie_id - 1]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        similar_movies.extend([movies.iloc[i[0]]['title'] for i in sim_scores[1:top_n + 1]])

    return list(set(similar_movies))

# Test content-based recommendation
recommend_content(1, top_n=5)

# Hybrid recommendation function
def hybrid_recommend(user_id, top_n=5, weight_collab=0.7, weight_content=0.3):
    # Collaborative Filtering recommendations
    collab_scores = {pred.iid: pred.est for pred in predictions if pred.uid == str(user_id)}

    # Content-Based recommendations
    content_recommendations = recommend_content(user_id, top_n=10)
    content_scores = {movies[movies['title'] == title].iloc[0]['movie_id']: 1 for title in content_recommendations}

    # Combine scores
    combined_scores = {}
    for movie_id in set(collab_scores.keys()).union(content_scores.keys()):
        combined_scores[movie_id] = (
            weight_collab * collab_scores.get(movie_id, 0) +
            weight_content * content_scores.get(movie_id, 0)
        )

    # Sort by combined score
    recommended_movie_ids = sorted(combined_scores, key=combined_scores.get, reverse=True)[:top_n]
    return [movies[movies['movie_id'] == movie_id].iloc[0]['title'] for movie_id in recommended_movie_ids]

# Test hybrid recommendation
hybrid_recommend(1, top_n=3)

from sklearn.metrics import precision_score

# Compute Precision@K
def precision_at_k(predictions, k=3):
    hits = 0
    for pred in predictions:
        if pred.est >= k and pred.r_ui >= k:
            hits += 1
    return hits / len(predictions)

precision = precision_at_k(predictions, k=3)
print(f"Precision@K (k=3): {precision:.4f}")

