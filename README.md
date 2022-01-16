# FeverScanner
A python script for an MLX90640/MLX90641 thermal imaging camera on the Raspberry Pi. This project is to create a fever scanner to monitor the users' body temperature. The users will scan their NFC tags to identify their IDs, then trigger the thermal imaging camera to start taking the body temperature.


# Requirements
There are a few libraries that this project requires:
* python-matplotlib, python-scipy, python-numpy, python-smbus through apt/dnf or pip
* RPI.GPIO, adafruit-blinka, adafruit-circuitpython-mlx90640 through pip
* Raspberry Pi
* NFC reader

# How to run it
* Start run.sh script on the Raspberry Pi. The script will monitor if the main progrom is running. Once the main progrom complete taking one person's body temperature, the main program will clear the information then exit by itself. The run.sh script will restart the main progrom.

# Credits
* This code was adapted from MakersPortal guide [here](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640)
* This project is following this https://www.youtube.com/watch?v=XRwbcsbh33w to set up. 
* The NFC setup is following this youtube https://www.youtube.com/watch?v=hhb7bCwYwnE.
* Forked from EverythingSmartHome/mlx90640-thermal-camera
