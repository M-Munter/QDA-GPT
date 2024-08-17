import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the AWS credentials and bucket information from .env
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# Initialize S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_S3_REGION_NAME)

try:
    # Upload the file
    s3.upload_file('test.png', AWS_STORAGE_BUCKET_NAME, 'test.png')
    print("Upload Successful")
except FileNotFoundError:
    print("The file was not found")
except NoCredentialsError:
    print("Credentials not available")
except Exception as e:
    print(f"An error occurred: {e}")
