import pandas as pd
import numpy as np
import pickle
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix


def preprocess_data(movies_path, ratings_path):
    """
    Loads and preprocesses the data by merging movies and ratings datasets.
    """
    print("🔄 Loading datasets...")

    # Load data
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)

    # Merge movies and ratings
    merged_df = pd.merge(ratings_df, movies_df, on="movieId")

    # Drop unnecessary columns
    merged_df = merged_df[["userId", "movieId", "rating"]]

    print(f"✅ Data preprocessing complete! {merged_df.shape[0]} ratings loaded.")

    return merged_df


def train_svd_model(data):
    """
    Trains an SVD recommendation model using Scipy's `svds`.
    """
    print("🚀 Training SVD model...")

    # Create user-movie matrix
    user_movie_matrix = data.pivot(
        index="userId", columns="movieId", values="rating"
    ).fillna(0)

    # Convert to sparse matrix format (CSR)
    user_movie_sparse = csr_matrix(user_movie_matrix.values)

    # Normalize matrix (mean centering)
    user_ratings_mean = user_movie_sparse.mean(axis=1).A1  # Convert to array
    normalized_matrix = user_movie_sparse - user_ratings_mean.reshape(-1, 1)

    # Convert to csr_matrix before passing to svds
    normalized_sparse = csr_matrix(normalized_matrix)

    # Perform SVD (k is the number of latent factors)
    U, sigma, Vt = svds(normalized_sparse, k=min(50, normalized_sparse.shape[1] - 1))
    sigma = np.diag(sigma)

    # Reconstruct the ratings matrix
    predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

    # Convert back to DataFrame
    predicted_df = pd.DataFrame(
        predicted_ratings,
        index=user_movie_matrix.index,
        columns=user_movie_matrix.columns,
    )

    print("✅ Model training complete!")

    return predicted_df


def save_model(model, model_path):
    """
    Saves the trained SVD model for future use.
    """
    import os

    # Ensure the models directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the model
    with open(model_path, "wb") as model_file:
        pickle.dump(model, model_file)

    print(f"💾 Model saved to {model_path}")


def recommend_movies(predicted_df, data, user_id, n_recommendations=5):
    """
    Generates top movie recommendations for a given user using SVD predictions.
    """
    print(f"🔎 Generating recommendations for User {user_id}...")

    # Get movie titles
    movies_df = pd.read_csv(movies_path)

    # Get predicted ratings for the user
    user_predictions = predicted_df.loc[user_id].sort_values(ascending=False)

    # Get movies the user has already rated
    user_rated_movies = data[data["userId"] == user_id]["movieId"].tolist()

    # Filter out already watched movies
    unseen_movies = user_predictions[
        ~user_predictions.index.isin(user_rated_movies)
    ].head(n_recommendations)

    # Get movie titles
    recommended_movies = movies_df[movies_df["movieId"].isin(unseen_movies.index)][
        ["movieId", "title"]
    ]

    print("🎬 Top recommended movies:")
    for index, row in recommended_movies.iterrows():
        print(f"🎥 {row['title']} (Movie ID: {row['movieId']})")

    return recommended_movies


if __name__ == "__main__":
    # File paths
    movies_path = "Dataset/movies.csv"
    ratings_path = "Dataset/ratings.csv"
    model_path = "models/svd_recommender.pkl"

    # Preprocess data
    data = preprocess_data(movies_path, ratings_path)

    # Train model
    svd_model = train_svd_model(data)

    # Save model
    save_model(svd_model, model_path)

    # Generate recommendations for a sample user
    sample_user_id = 1
    recommend_movies(svd_model, data, sample_user_id)
