# Importing all the libraries
import pandas as pd
import numpy as np
import pickle
import boto3
import io
import logging
import os
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define S3 bucket and file path
BUCKET_NAME = "rahul-movie-recommendation-data"  # Replace with your S3 bucket name
PREPROCESSED_DATA_KEY = "processed/preprocessed_data.csv"  # S3 key for processed data


def load_data_from_s3():
    """
    Loads the preprocessed dataset from S3.

    Returns:
        pd.DataFrame: The preprocessed dataset.

    Raises:
        Exception: If the dataset cannot be downloaded.
    """
    logging.info(f"Downloading {PREPROCESSED_DATA_KEY} from S3...")
    s3 = boto3.client("s3")

    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=PREPROCESSED_DATA_KEY)
        df = pd.read_csv(io.BytesIO(obj["Body"].read()))
        logging.info("Successfully downloaded preprocessed data from S3.")
        return df
    except Exception as e:
        logging.error(f"Error: Could not download preprocessed data from S3: {e}")
        raise


def train_svd_model():
    """
    Trains an SVD recommendation model using Scipy's `svds`.

    Returns:
        pd.DataFrame: The predicted ratings matrix.

    Raises:
        Exception: If the training process fails.
    """
    try:
        data = load_data_from_s3()
    except Exception:
        logging.error("Exiting: Failed to load data from S3.")
        return

    logging.info("Training SVD model...")

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
    try:
        U, sigma, Vt = svds(
            normalized_sparse, k=min(50, normalized_sparse.shape[1] - 1)
        )
        sigma = np.diag(sigma)
    except Exception as e:
        logging.error(f"Error during SVD computation: {e}")
        return

    # Reconstruct the ratings matrix
    predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

    # Convert back to DataFrame
    predicted_df = pd.DataFrame(
        predicted_ratings,
        index=user_movie_matrix.index,
        columns=user_movie_matrix.columns,
    )

    logging.info("Model training complete. Saving model...")

    # Save trained model
    save_model(predicted_df)

    return predicted_df


def save_model(model):
    """
    Saves the trained SVD model for future use.

    Args:
        model (pd.DataFrame): The trained recommendation model.

    Raises:
        Exception: If the model cannot be saved.
    """
    model_path = "Scripts/models/svd_recommender.pkl"

    try:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, "wb") as model_file:
            pickle.dump(model, model_file)
        logging.info(f"Model saved to {model_path}")
    except Exception as e:
        logging.error(f"Error saving model: {e}")
        raise


def recommend_movies(user_id=1, n_recommendations=5):
    """
    Generates top movie recommendations for a given user.

    Args:
        user_id (int, optional): The user ID for recommendations. Defaults to 1.
        n_recommendations (int, optional): Number of movies to recommend. Defaults to 5.

    Returns:
        pd.DataFrame: A DataFrame containing recommended movies.

    Raises:
        Exception: If the recommendation process fails.
    """

    logging.info(f"Generating recommendations for User {user_id}...")

    # Load the trained model
    model_path = "Scripts/models/svd_recommender.pkl"
    try:
        with open(model_path, "rb") as model_file:
            predicted_df = pickle.load(model_file)
    except Exception as e:
        logging.error(f"Error loading trained model: {e}")
        return

    # Load dataset again (as we need movie titles)
    try:
        data = load_data_from_s3()
    except Exception:
        logging.error("Error: Could not load preprocessed data for recommendations.")
        return

    # Get predicted ratings for the user
    try:
        user_predictions = predicted_df.loc[user_id].sort_values(ascending=False)
    except KeyError:
        logging.error(f"User ID {user_id} not found in the dataset.")
        return

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

    logging.info("Top recommended movies:")
    for index, row in recommended_movies.iterrows():
        logging.info(f"{row['title']} (Movie ID: {row['movieId']})")

    return recommended_movies
