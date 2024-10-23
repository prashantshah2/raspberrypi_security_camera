
import os
import time
import socket
from gpiozero import MotionSensor
from datetime import datetime
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from aws_s3 import AWSUtils
from send_smtp_gmail import send_smtp_gmail
from jproperties import Properties

def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def send_sms(sms_body):
    send_smtp_gmail(sender_email, to_email, password, subject, sms_body)

def take_picture(image_file):
    picam2.start()

    print(current_time() + " Taking picture")
    picam2.capture_file(image_file)
    print(current_time() + " Picture taken")
   
    picam2.stop()

def take_video(video_file):
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)

    print(current_time() + " Recording video to " + video_file)
    picam2.start_and_record_video(video_file, duration=5, quality=Quality.LOW)
    # encoder = H264Encoder(10000000)
    # output = FfmpegOutput('test.mp4')

    # picam2.start_recording(encoder, output)
    time.sleep(3)
    print(current_time() + " Stop recording video")
    picam2.stop_recording()
    #picam2.stop_preview()

def upload_to_s3(source_file, bucket_name, s3_file_name):
    awsUtils = AWSUtils()
    awsUtils.upload_image_to_s3(source_file, bucket_name, s3_file_name)


# config parameters
project_dir = ""
bucket = ""
sender_email = ""
to_email = ""
subject = "Motion Detected"
password = os.environ.get('MAIL_APP_PASSWORD')

is_headless = True
demo_mode = False

picam2 = Picamera2()

# Create a new object, camera_config and use it to set the still 
# image resolution (main) to 1920 x 1080. and 
# a “lowres” image with a size of 640 x 480. 
# This lowres image is used as the preview image when framing a shot.
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, 
                                                  lores={"size": (640, 480)}, 
                                                  display="lores")
picam2.configure(camera_config)
    
configs = Properties()

with open('app-config.properties', 'rb') as config_file:
    configs.load(config_file)

sender_email = configs.get("FROM_EMAIL").data
to_email = configs.get("TO_EMAIL").data
password = os.environ.get('MAIL_APP_PASSWORD')
project_dir = configs.get("PROJECT_DIR").data
bucket = configs.get("BUCKET").data

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
motion_sensor = MotionSensor(12) # out plugged into GPIO12
try:
    while True:
        print(current_time() + " Continue scanning for motion...")

        # Wait for motion detection
        motion_sensor.wait_for_motion()

        print(current_time() + " motion detected!")

        # Turn LED ON
        GPIO.output(7,True)

        if (is_headless):
            picam2.start_preview(Preview.NULL)
        else: 
            picam2.start_preview(Preview.QT)

        # initialize output image and video file names
        timeStr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') 
        tStr = datetime.now().strftime('%H:%M:%S %p')
        ifilename = "motion-image-" + timeStr + ".jpg"
        image_file = project_dir + "/output/" + ifilename
        s3_image_file = "images/" + ifilename

        take_picture(image_file)

        vfilename = "motion_video-" + timeStr + ".mp4"
        video_file = project_dir + "/output/" + vfilename
        s3_video_file = "images/" + vfilename

        take_video(video_file)

        upload_to_s3(video_file, bucket, s3_video_file)
        upload_to_s3(image_file, bucket, s3_image_file)

        sms_body = 'Raspberry PI ({}): Motion detected at {}'.format(socket.gethostname(), tStr)
        send_sms(sms_body)

        # if in demo mode, let preview run
        if (demo_mode == True):
            time.sleep(5)
        
        picam2.stop_preview()

        # wait for motion sensor to be idle for configured interval
        motion_sensor.wait_for_no_motion()
        print(current_time() + " motion stopped ...")

        # turn LED off
        GPIO.output(7,False)
except KeyboardInterrupt:
    # Clean up resources
    motion_sensor.close()

GPIO.cleanup()


