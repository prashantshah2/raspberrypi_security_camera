# A DIY Security System using Raspberry Pi and AWS
## Solution
Refer to [details here](https://share.merck.com/display/~shprash2/Tech+Showcase)

## Needed for Projects

- A [Raspberry PI](https://www.raspberrypi.com/) (cB+, 4 or Zero 2 W )
- An official [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)
- PIR Motion Sensor Module (HC-SR501)
- A [mini breadboard](https://www.amazon.com/Qunqi-point-Experiment-Breadboard-5-5%C3%978-2%C3%970-85cm/dp/B0135IQ0ZC?tag=georiot-us-default-20&ascsubtag=tomshardware-us-1113933765553713669-20&geniuslink=true)
- [Female to male wires](https://www.amazon.com/ELOOGAA-Multicolored-Breadboard-Compatible-Projects/dp/B0BGSFGSBJ/ref=sr_1_6?dib=eyJ2IjoiMSJ9.tjHxIQLJsk16_0YVtUGN6Qr9ToaNYxpqXSHXwBOq_th-Yd0E2Mvw02Vhg3KFdVn21ueotYn_oI7g3wO9nVPOzWBslgV9Qp2-v-ZWK2JYV7qecNS1nXDy788ITYVCRX348xBjKN4mcgx2J1CLAV-IZqRDnNLv5jBfiCwqxWt3EGv2zGE1G22kIrdkUaTke5BhFAg6IVZx2_aWVsMZQJYCyIlYwRP3YJfSxwnWzxxru9r-yhjmGiPJ877And581ecVTiOqhXr0Ng1GFku-n0UFGns4w9hRwAmYEoABngrg6qI.G3tEZUE1KqOX-EMZVwRJky6Gh-6ZdlkWicrR520FdeI&dib_tag=se&keywords=female+to+male+wires&qid=1729636556&s=industrial&sr=1-6)
- Mini SD Card
- AWS Account

## Prepare Raspberry PI

- Set up a Raspberry Pi. Install an operating system on SD card. [Refer to getting started guide](https://www.raspberrypi.com/documentation/computers/getting-started.html).
- [Connect the Camera](https://www.raspberrypi.com/documentation/accessories/camera.html#:~:text=an%20earthing%20strap.-,Connect%20the%20Camera,contacts%20facing%20the%20HDMI%20port.)
- [Connect PIR Motion Sensor](https://projects.raspberrypi.org/en/projects/physical-computing/11)
- [Connect LED](https://projects.raspberrypi.org/en/projects/physical-computing/2)
## Install libraries
- Install required System Packages libraries
```
    sudo apt install -y python3-picamera2
    sudo apt install xrdp -y
```

- Install required python packages (boto3, picamera, gpiozero, RPi.GPIO)
```
pip3 install -r requirements.txt
```
or
```
pip3 install boto3 picamera gpiozero RPi.GPIO
```

## Define AWS Lambda function
Follow [AWS guide here](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html) to define labda function with s3 trigger
