import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Ensure the following environment variables are set
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

image_dir="/home/pi/dev/test/output"
image_file_name = "test2.jpg"
image_path = image_dir + "/" + image_file_name

def upload_image_to_s3(file_path, bucket_name, s3_file_name=None):
    try:
        # Initialize the S3 client
        s3 = boto3.client('s3')

        if s3_file_name is None:
            s3_file_name = os.path.basename(file_path)

        # Upload the file
        s3.upload_file(file_path, bucket_name, s3_file_name)
        print(f'File {file_path} uploaded to {bucket_name}/{s3_file_name}')
    except FileNotFoundError:
        print('The file was not found')
    except NoCredentialsError:
        print('Credentials not available')
    except PartialCredentialsError:
        print('Incomplete credentials provided')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    file_path = image_path      # Local path to the image
    bucket_name = 'pshah-pi3/images'       # Name of your S3 bucket
    s3_file_name = 'uploaded_image.jpg'       # S3 object name

    upload_image_to_s3(file_path, bucket_name)