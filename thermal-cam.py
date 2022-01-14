#! /usr/bin/python3
import time,board,busio
import numpy as np
import adafruit_mlx90640
import RPi.GPIO as GPIO



i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate

frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
i = 1

while i < 6:
    try:
       
        
        mlx.getFrame(frame) # read MLX temperatures into frame var
        # figure out how to puse for one second
        print('Please wait the device is warming up...')
        time.sleep(3.0)
        i += 1
        break
    except ValueError:
        print('error getting frame from thermal camera issue')
        continue # if error, just read again

# print out the average tem perature from the MLX90640
print('Max MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.\
      format(np.max(frame),(((9.0/5.0)*np.max(frame))+32.0)))


 
if np.max(frame) > 38.5:
   

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)

    print('Red Light on')
                # GPIO.output(17,GPIO.HIGH)
                # sleep(5.0)
    GPIO.output(18,GPIO.HIGH)
    time.sleep(5.5)
    GPIO.output(18,GPIO.LOW)
    GPIO.cleanup()
elif np.max(frame) <= 38.5:
                
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.OUT)

    print('Light on')
    # GPIO.output(17,GPIO.HIGH)
    # sleep(5.0)
    GPIO.output(17,GPIO.HIGH)
    time.sleep(5.5)

    GPIO.output(17,GPIO.LOW)
    GPIO.cleanup()

                    

