import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.config import Config

# Ensure the following environment variables are set
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

class AWSUtils:
    def generate_signed_url(self, bucket_name, object_name, expiration=3600):
        try:
            # Initialize the S3 client
            config = Config(signature_version='s3v4')
            s3_client = boto3.client('s3', config=config)
            response = s3_client.generate_presigned_url('get_object',
                        Params={'Bucket': bucket_name, 
                                'Key': object_name}, ExpiresIn=expiration)
            print(f'{bucket_name}/{object_name} signed url = {response}')
            # return signed_url
            return response
        except Exception as e:
            print(f'An error generating presigned url: {e}')   
            raise

    def upload_image_to_s3(self, file_path, bucket_name, s3_file_name=None):
        try:
            # Initialize the S3 client
            s3 = boto3.client('s3')

            if s3_file_name is None:
                s3_file_name = os.path.basename(file_path)

            # Upload the file
            s3.upload_file(file_path, bucket_name, s3_file_name)
            print(f'File {file_path} uploaded to {bucket_name}/{s3_file_name}')
        except FileNotFoundError:
            print(f'Upload error: The file {file_path} was not found')
            raise
        except NoCredentialsError:
            print('Upload error: Credentials not available')
            raise
        except PartialCredentialsError:
            print('Upload error: Incomplete credentials provided')
            raise
        except Exception as e:
            print(f'An error occurred: {e}')
            raise

if __name__ == '__main__':

    #image_path="/home/pi/dev/test/output/test2.jpg"
    image_path = "/Users/shprash2/Downloads/test3.png"
    file_path = image_path      # Local path to the image
    bucket_name = 'pshah-pi3'       # Name of your S3 bucket
    s3_file_name = 'images/uploaded_image.jpg'       # S3 object name

    awsUtils = AWSUtils()
    #awsUtils.upload_image_to_s3(file_path, bucket_name, s3_file_name)
    awsUtils.generate_signed_url(bucket_name, s3_file_name)