#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

print"Light on"
# GPIO.output(17,GPIO.HIGH)
# sleep(5.0)
GPIO.output(18,GPIO.HIGH)
time.sleep(5.5)

GPIO.output(18,GPIO.LOW)
GPIO.cleanup()
