import os
from dotenv import load_dotenv  # Import the load_dotenv function
import boto3
from flask import Flask, render_template_string

# Load the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Retrieve AWS credentials and bucket information from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name=AWS_S3_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

@app.route('/')
def show_image():
    # Define the object key (path to your file in S3)
    object_key = 'media/flowcharts/flowchart.png'

    # Generate the URL for the object
    url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{object_key}"

    # Render a simple HTML page showing the image
    html_content = f"""
    <html>
        <body>
            <h1>Flowchart Image</h1>
            <img src="{url}" alt="Flowchart Image" style="max-width:100%;">
        </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
