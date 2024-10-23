# https://www.youtube.com/watch?v=Q4_i5j64hdw
# https://www.tomshardware.com/how-to/use-picamera2-take-photos-with-raspberry-pi

import RPi.GPIO as GPIO
import time
from datetime import datetime

# GPIO pin setup
PIR_PIN = 12
LED_PIN = 23

def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def pir2():
    # Create a MotionSensor object using GPIO pin 12
    motion_sensor = MotionSensor(12)

    try:
        while True:
            # Wait for motion to be detected
            motion_sensor.wait_for_motion()

            print("Motion detected!")

            # Wait for a short delay to avoid multiple detections
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Clean up resources
        motion_sensor.close()


# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up PIR sensor pin as input
GPIO.setup(PIR_PIN, GPIO.IN)

# Set up LED pin as output
GPIO.setup(LED_PIN, GPIO.OUT)

# Initial state of PIR sensor
motion_detected = False

# Timer for inactivity
inactivity_timer = 0

try:
    while True:
        # Read PIR sensor value
        if GPIO.input(PIR_PIN):
            # Motion detected
            print(current_time() + " Motion detected")
            motion_detected = True
            inactivity_timer = 0
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            # No motion detected
            print(current_time() + " No motion detected")
            motion_detected = False
            inactivity_timer += 1

            # If no motion for 5 seconds, send signal (replace with your desired action)
            if inactivity_timer >= 5:
                print(current_time() + " No motion detected for 5 seconds")
                # Your signal sending code here

        # Update LED state based on motion
        GPIO.output(LED_PIN, motion_detected)

        # Delay for a short time to avoid excessive CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up GPIO pins
    GPIO.cleanup()
