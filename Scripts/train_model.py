import pandas as pd
import numpy as np
import pickle
import boto3
import io
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# Define S3 bucket and file path
BUCKET_NAME = "rahul-movie-recommendation-data"  # Replace with your S3 bucket name
PREPROCESSED_DATA_KEY = "processed/preprocessed_data.csv"  # S3 key for processed data


def load_data_from_s3():
    """
    Loads the preprocessed dataset from S3.
    """
    print(f"🔄 Downloading {PREPROCESSED_DATA_KEY} from S3...")
    s3 = boto3.client("s3")

    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=PREPROCESSED_DATA_KEY)
        df = pd.read_csv(io.BytesIO(obj["Body"].read()))
        print("✅ Successfully downloaded preprocessed data from S3.")
        return df
    except Exception as e:
        print(f"❌ Error: Could not download preprocessed data from S3: {e}")
        return None


def train_svd_model():
    """
    Trains an SVD recommendation model using Scipy's `svds`.
    """
    data = load_data_from_s3()
    if data is None:
        print("❌ Exiting: Failed to load data from S3.")
        return

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

    # Save trained model
    save_model(predicted_df)

    return predicted_df


def save_model(model):
    """
    Saves the trained SVD model for future use.
    """
    model_path = "models/svd_recommender.pkl"

    import os

    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    with open(model_path, "wb") as model_file:
        pickle.dump(model, model_file)

    print(f"💾 Model saved to {model_path}")


def recommend_movies(user_id=1, n_recommendations=5):
    """
    Generates top movie recommendations for a given user using SVD predictions.
    """
    print(f"🔎 Generating recommendations for User {user_id}...")

    # Load the trained model
    model_path = "models/svd_recommender.pkl"
    with open(model_path, "rb") as model_file:
        predicted_df = pickle.load(model_file)

    # Load dataset again (as we need movie titles)
    data = load_data_from_s3()
    if data is None:
        print("❌ Error: Could not load preprocessed data for recommendations.")
        return

    # Get predicted ratings for the user
    user_predictions = predicted_df.loc[user_id].sort_values(ascending=False)

    # Get movies the user has already rated
    user_rated_movies = data[data["userId"] == user_id]["movieId"].tolist()

    # Filter out already watched movies
    unseen_movies = user_predictions[
        ~user_predictions.index.isin(user_rated_movies)
    ].head(n_recommendations)

    # Get movie titles
    recommended_movies = data[data["movieId"].isin(unseen_movies.index)][
        ["movieId", "title"]
    ].drop_duplicates()

    print("🎬 Top recommended movies:")
    for index, row in recommended_movies.iterrows():
        print(f"🎥 {row['title']} (Movie ID: {row['movieId']})")

    return recommended_movies
