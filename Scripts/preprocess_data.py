import boto3
import pandas as pd
import io
import os

def preprocess_data():
    try:
        # Initialize the S3 client
        s3 = boto3.client("s3")

        # Define the S3 bucket name
        bucket_name = "rahul-movie-recommendation-data"  # Replace with your S3 bucket

        # Define the S3 keys for raw data
        raw_movies_key = "raw/movies.csv"
        raw_ratings_key = "raw/ratings.csv"

        # Define the S3 key for the processed data
        preprocessed_key = "processed/preprocessed_data.csv"

        print("✅ Starting data preprocessing...")

        # Download movies.csv from S3
        print(f"🔄 Downloading {raw_movies_key} from S3...")
        try:
            movies_obj = s3.get_object(Bucket=bucket_name, Key=raw_movies_key)
            movies_df = pd.read_csv(io.BytesIO(movies_obj["Body"].read()))
            print("✅ Successfully downloaded movies.csv")
        except Exception as e:
            print(f"❌ Error: Could not download movies.csv: {e}")
            return

        # Download ratings.csv from S3
        print(f"🔄 Downloading {raw_ratings_key} from S3...")
        try:
            ratings_obj = s3.get_object(Bucket=bucket_name, Key=raw_ratings_key)
            ratings_df = pd.read_csv(io.BytesIO(ratings_obj["Body"].read()))
            print("✅ Successfully downloaded ratings.csv")
        except Exception as e:
            print(f"❌ Error: Could not download ratings.csv: {e}")
            return

        # Merge movies and ratings data
        print("🔄 Merging datasets...")
        merged_df = pd.merge(ratings_df, movies_df, on="movieId")

        # Handle missing values
        merged_df.dropna(inplace=True)

        # Save preprocessed data to a temporary directory
        local_preprocessed_path = "/tmp/preprocessed_data.csv"
        print(f"🔄 Saving preprocessed data to {local_preprocessed_path}...")
        merged_df.to_csv(local_preprocessed_path, index=False)
        print("✅ Successfully saved preprocessed data locally.")

        # Upload the preprocessed data back to S3
        print(f"🔄 Uploading processed data to s3://{bucket_name}/{preprocessed_key}...")
        s3.upload_file(local_preprocessed_path, bucket_name, preprocessed_key)
        print(f"✅ Preprocessed data uploaded to s3://{bucket_name}/{preprocessed_key}")

    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
