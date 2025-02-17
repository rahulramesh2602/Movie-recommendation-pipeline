# Importing all libraries
import boto3
import pandas as pd
import io
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def preprocess_data():
    """
    Downloads raw movie and rating datasets from S3,
    merges them and processes missing values,
    and uploads the preprocessed dataset back to S3.

    Raises:
        Exception: If any step in the process fails.
    """
    try:
        # Initialize the S3 client
        s3 = boto3.client("s3")

        # Define S3 bucket name
        bucket_name = "rahul-movie-recommendation-data"  # Update with you bucket name

        # Define S3 keys for raw and processed data
        raw_movies_key = "raw/movies.csv"
        raw_ratings_key = "raw/ratings.csv"
        preprocessed_key = "processed/preprocessed_data.csv"

        logging.info("Starting data preprocessing...")

        # Download movies.csv from S3
        try:
            logging.info(f"Downloading {raw_movies_key} from S3...")
            movies_obj = s3.get_object(Bucket=bucket_name, Key=raw_movies_key)
            movies_df = pd.read_csv(io.BytesIO(movies_obj["Body"].read()))
            logging.info("Successfully downloaded movies.csv")
        except Exception as e:
            logging.error(f"Error: Could not download movies.csv: {e}")
            raise

        # Download ratings.csv from S3
        try:
            logging.info(f"Downloading {raw_ratings_key} from S3...")
            ratings_obj = s3.get_object(Bucket=bucket_name, Key=raw_ratings_key)
            ratings_df = pd.read_csv(io.BytesIO(ratings_obj["Body"].read()))
            logging.info("Successfully downloaded ratings.csv")
        except Exception as e:
            logging.error(f"Error: Could not download ratings.csv: {e}")
            raise

        # Merge movies and ratings data
        logging.info("Merging datasets...")
        merged_df = pd.merge(ratings_df, movies_df, on="movieId")

        # Handle missing values
        merged_df.dropna(inplace=True)

        # Save preprocessed data to a temporary directory
        local_preprocessed_path = "/tmp/preprocessed_data.csv"
        logging.info(f"Saving preprocessed data to {local_preprocessed_path}...")
        merged_df.to_csv(local_preprocessed_path, index=False)
        logging.info("Successfully saved preprocessed data locally.")

        # Upload the preprocessed data back to S3
        logging.info(
            f"Uploading processed data to s3://{bucket_name}/{preprocessed_key}..."
        )
        s3.upload_file(local_preprocessed_path, bucket_name, preprocessed_key)
        logging.info(
            f"Preprocessed data uploaded to s3://{bucket_name}/{preprocessed_key}"
        )

    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        raise
