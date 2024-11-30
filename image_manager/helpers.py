"""
This file has all the utilities functions for image manager app
"""
import os
from io import BytesIO

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")


def upload_file_to_s3(file, file_name):
    """
    Upload a file to S3 with temporary storage if needed.
    """

    if isinstance(file, BytesIO):
        file.seek(0)

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    try:
        s3_client.upload_fileobj(file, s3_bucket_name, file_name)
        s3_url = f"s3://{s3_bucket_name}/{file_name}"

        return s3_url
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
