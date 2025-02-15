# Importing all libraries
import boto3
import os


def upload_to_s3():
    # Initialize the S3 client
    s3 = boto3.client("s3")

    # Define the S3 bucket name
    bucket_name = "rahul-movie-recommendation-data"

    # Define the local paths to the dataset files
    local_movies_path = "Dataset/movies.csv"
    local_ratings_path = "Dataset/ratings.csv"

    # Define the S3 paths where the files will be uploaded
    s3_movies_key = "raw/movies.csv"
    s3_ratings_key = "raw/ratings.csv"

    try:
        # Upload movies.csv to S3
        s3.upload_file(local_movies_path, bucket_name, s3_movies_key)
        print(f"Uploaded {local_movies_path} to s3://{bucket_name}/{s3_movies_key}")

        # Upload ratings.csv to S3
        s3.upload_file(local_ratings_path, bucket_name, s3_ratings_key)
        print(f"Uploaded {local_ratings_path} to s3://{bucket_name}/{s3_ratings_key}")

    except Exception as e:
        print(f"Error uploading files to S3: {e}")
