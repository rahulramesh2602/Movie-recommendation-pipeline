import boto3
import pandas as pd
import io


def preprocess_data():
    # Initialize the S3 client
    s3 = boto3.client("s3")

    # Define the S3 bucket name
    bucket_name = "rahul-movie-recommendation-data"  # Replace with your S3 bucket name

    # Define the S3 keys for the raw data
    raw_movies_key = "raw/movies.csv"
    raw_ratings_key = "raw/ratings.csv"

    # Define the S3 key for the preprocessed data
    preprocessed_key = "processed/preprocessed_data.csv"

    try:
        # Download movies.csv from S3
        movies_obj = s3.get_object(Bucket=bucket_name, Key=raw_movies_key)
        movies_df = pd.read_csv(io.BytesIO(movies_obj["Body"].read()))

        # Download ratings.csv from S3
        ratings_obj = s3.get_object(Bucket=bucket_name, Key=raw_ratings_key)
        ratings_df = pd.read_csv(io.BytesIO(ratings_obj["Body"].read()))

        # Example: Merge movies and ratings data
        merged_df = pd.merge(ratings_df, movies_df, on="movieId")

        # Example: Handle missing values (if any)
        merged_df.dropna(inplace=True)

        # Save the preprocessed data to a local file
        local_preprocessed_path = "preprocessed_data.csv"
        merged_df.to_csv(local_preprocessed_path, index=False)

        # Upload the preprocessed data to S3
        s3.upload_file(local_preprocessed_path, bucket_name, preprocessed_key)
        print(f"Preprocessed data uploaded to s3://{bucket_name}/{preprocessed_key}")

    except Exception as e:
        print(f"Error during preprocessing: {e}")


if __name__ == "__main__":
    preprocess_data()
