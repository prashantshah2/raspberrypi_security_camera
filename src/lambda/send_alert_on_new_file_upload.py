import json
import urllib.parse
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.config import Config
from datetime import datetime

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

print('Loading function')

# AWS SES configuration
AWS_REGION = "us-east-1"
SENDER = "pshahmrk1@gmail.com"
RECIPIENT = "prashant.shah1@merck.com"
SUBJECT = "Email Subject"
BODY_TEXT = "Hello,\n\nThis is a test email with an image attachment."
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Hello!</h1>
  <p>This is a test email with an image attachment.</p>
</body>
</html>
"""

SUBJECT_ARGS = "Motion detected at %s"
BODY_TEXT_ARGS = ("Motion detected\r\n"
            "Bucket: %s\r\n"
            "File: %s\r\n"
            "Date: %s at %s\r\n"
            "Photo: %s\r\n"
            )
BODY_HTML_ARGS = """<html>
<head></head>
<body>
<h1>Motion Detected using Raspberry PI</h1>
<p style="line-height: 1.1">Details:</p>
Bucket: %s<br>
File: %s<br>
Date: %s at %s<br>
<a href='%s'/>Click here to get photo</a><br>
Here's Image:
<img src="cid:%s">
</body>
</html>
            """    

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
            return response
        except Exception as e:
            print(f'An error generating presigned url: {e}')   
            raise

    def send_raw_email(self, bucket, key, date, time, signed_url):
        # Create a new SES client
        client = boto3.client('ses', region_name=AWS_REGION)

        email_subject = SUBJECT_ARGS % (time)
        # The email body for recipients with non-HTML email clients.
        email_body_plain_text = BODY_TEXT_ARGS % (bucket, key, date, time, signed_url)

        attachment_name = key.rsplit('/')[1]
        # The HTML body of the email.
        email_body_html = BODY_HTML_ARGS % (bucket, key, date, time, signed_url, attachment_name)

        # Create a multipart/mixed parent container
        msg = MIMEMultipart('mixed')
        msg['Subject'] = email_subject
        msg['From'] = SENDER
        msg['To'] = RECIPIENT

        # Create a multipart/alternative child container
        msg_body = MIMEMultipart('alternative')
        
        # Encodes the text and HTML versions of the email body
        textpart = MIMEText(email_body_plain_text, 'plain')
        htmlpart = MIMEText(email_body_html, 'html')
        
        # Add the text and HTML parts to the child container
        msg_body.attach(textpart)
        msg_body.attach(htmlpart)
        
        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container
        msg.attach(msg_body)
        
        # Retrieve and Attach the image
        config = Config(signature_version='s3v4')
        s3_client = boto3.client('s3', config=config)
        fname = key.rsplit('/')[1]
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response['Body'].read()
        image = MIMEImage(body)
        image.add_header('Content-Disposition', 'attachment', filename=fname)
        msg.attach(image)
        
        # # Attach the image
        # with open(IMAGE_PATH, 'rb') as image_file:
        #     image = MIMEImage(image_file.read())
        #     image.add_header('Content-Disposition', 'attachment', filename="image.jpg")
        #     msg.attach(image)
        
        try:
            # Provide the contents of the email
            response = client.send_raw_email(
                Source=SENDER,
                Destinations=[RECIPIENT],
                RawMessage={
                    'Data': msg.as_string(),
                },
            )
        except Exception as e:
            print(f"Error: {e}")
        else:
            print("Email with attachment sent! Message ID:"),
            print(response['MessageId'])

    def send_email(self, bucket, key):
        import boto3
        from botocore.exceptions import ClientError

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the 
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        #CONFIGURATION_SET = "ConfigSet"

        # The subject line for the email.
        #SUBJECT = "Amazon SES Test (SDK for Python)"

        email_subject = SUBJECT_ARGS % ("2:45PM")
        # The email body for recipients with non-HTML email clients.
        email_body_plain_text = BODY_TEXT_ARGS % ((bucket, key, "2014-10-21", "https://amazon.com"))

        # The HTML body of the email.
        email_body_html = BODY_HTML_ARGS % (bucket, key, "2014-10-21", "https://amazon.com")

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses',region_name=AWS_REGION)

        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': email_body_html,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': email_body_plain_text,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': email_subject,
                    },
                },
                Source=SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
                #ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
            return response['MessageId']

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(f"Bucket Name={bucket}, key={key}")
    try:
        #response = s3.get_object(Bucket=bucket, Key=key)
        #print("CONTENT TYPE: " + response['ContentType'])
        awsUtils = AWSUtils()
        signed_url = awsUtils.generate_signed_url(bucket, key)
        today = datetime.today()
        dateStr = today.strftime("%m/%d/%y")
        
        now = datetime.now()
        timeStr = now.strftime("%H:%M:%S")
        msgId = awsUtils.send_raw_email(bucket, key, dateStr, timeStr, signed_url)
        return msgId
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


if __name__ == "__main__":
    bucket="pshahmrk1"
    key="images/image2.jpg"

    today = datetime.today()
    dateStr = today.strftime("%m/%d/%y")
    
    now = datetime.now()
    timeStr = now.strftime("%H:%M:%S")

    awsUtils = AWSUtils()
    signed_url = awsUtils.generate_signed_url(bucket, key)
    awsUtils.send_raw_email(bucket, key, dateStr, timeStr, signed_url)