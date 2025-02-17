# Importing all libraries
import boto3
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def upload_to_s3():
    """
    Uploads dataset files to an Amazon S3 bucket.

    This function uploads `movies.csv` and `ratings.csv`
    from the local `Dataset/` directory
    to the specified S3 bucket under the `raw/` prefix.

    Raises:
        FileNotFoundError: If a dataset file is missing locally.
        Exception: If the upload to S3 fails.
    """
    # Initialize S3 client
    s3 = boto3.client("s3")

    # Define S3 bucket name
    bucket_name = "rahul-movie-recommendation-data"

    # Define local file paths and corresponding S3 paths
    local_movies_path = "Dataset/movies.csv"
    local_ratings_path = "Dataset/ratings.csv"
    s3_movies_key = "raw/movies.csv"
    s3_ratings_key = "raw/ratings.csv"

    # Check if files exist before uploading
    if not os.path.exists(local_movies_path):
        raise FileNotFoundError(f"File not found: {local_movies_path}")

    if not os.path.exists(local_ratings_path):
        raise FileNotFoundError(f"File not found: {local_ratings_path}")

    try:
        # Upload movies.csv to S3
        logging.info(
            f"Uploading {local_movies_path} to s3://{bucket_name}/{s3_movies_key}..."
        )
        s3.upload_file(local_movies_path, bucket_name, s3_movies_key)
        logging.info(f"Upload successful: s3://{bucket_name}/{s3_movies_key}")

        # Upload ratings.csv to S3
        logging.info(
            f"Uploading {local_ratings_path} to s3://{bucket_name}/{s3_ratings_key}..."
        )
        s3.upload_file(local_ratings_path, bucket_name, s3_ratings_key)
        logging.info(f"Upload successful: s3://{bucket_name}/{s3_ratings_key}")

    except Exception as e:
        logging.error(f"Error uploading files to S3: {e}")
        raise
