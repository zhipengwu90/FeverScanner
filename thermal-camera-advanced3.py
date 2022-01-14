#! /usr/bin/python3
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
from scipy import ndimage
import argparse
from tkinter import *
from tkinter.messagebox import Message
from _tkinter import TclError
import threading
import time
from guizero import App, Box, Text, TextBox, warn
import csv


parser = argparse.ArgumentParser(description='Thermal Camera Program')
parser.add_argument('--mirror', dest='imageMirror', action='store_const', default='false',
                    const='imageMirror', help='Flip the image for selfie (default: false)')
args = parser.parse_args()
imageMirror = args.imageMirror

if(imageMirror == 'false'):
    print('Mirror mode: false')
else:
    imageMirror = 'true'
    print('Mirror mode: true')


i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # set refresh rate
mlx_shape = (24,32) # mlx90640 shape

mlx_interp_val = 10 # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val) # new shape

fig = plt.figure(figsize=(5,3)) # start figure 12,9
ax = fig.add_subplot(111) # add subplot
fig.subplots_adjust(0.05,0.05,0.95,0.95) # get rid of unnecessary padding
therm1 = ax.imshow(np.zeros(mlx_interp_shape),interpolation='none',
                   cmap=plt.cm.bwr,vmin=25,vmax=45) # preemptive image
cbar = fig.colorbar(therm1) # setup colorbar
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

fig.canvas.draw() # draw figure to copy background
ax_background = fig.canvas.copy_from_bbox(ax.bbox) # copy background
ax.text(-75, 125, 'Max:', color='red')
textMaxValue = ax.text(-75, 150, 'test1', color='black')
fig.show() # show the figure before blitting

frame = np.zeros(mlx_shape[0]*mlx_shape[1]) # 768 pts

def clearDisplay():
    print("Clear display")
    rfidStatus.value = "---"
    rfidText.value = ""
#     led8.off()
    rfidStatus.repeat(1000, checkRFidTag)

def checkRFidTag():
    tagId = rfidText.value
    if tagId != "":
        RFidRegistered = False
        print(tagId)
        with open("Database.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["RFid"] == tagId:
                    RFidRegistered = True
                    print("Welcome " + row["User"])
                    rfidStatus.value = "Welcome " + row["User"]
#                     led8.on()
                    rfidStatus.after(3000, clearDisplay)
                    
                 
        if RFidRegistered == False:
            print("RFid tag is not registered")
            rfidStatus.value = "RFid tag is not registered"
            rfidStatus.after(3000, clearDisplay)
        
        rfidStatus.cancel(checkRFidTag)



t0=time.time()



def body_temp():
    TIME_TO_WAIT = 3000
    root = Tk()
    root.withdraw()
    try:
        root.after(TIME_TO_WAIT, root.destroy)
        Message(title="Please wait", message="Proccessing your body temperature,pleas don't move", master=root).show()
        mlx.getFrame(frame) # read MLX temperatures into frame var
                # figure out how to puse for one second
       
        print('Please wait the device is warming up...')
        
            # print out the average tem perature from the MLX90640
        print('Max MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.\
        format(np.max(frame),(((9.0/5.0)*np.max(frame))+32.0)))
            
    except ValueError:
        print('error getting frame from thermal camera issue')
         # if error, just read again
  
    if np.max(frame) > 38.5:
        TIME_TO_WAIT = 5000
        root = Tk()
        root.withdraw()
        try:
            root.after(TIME_TO_WAIT, root.destroy)
            Message(title="Warming", message="You may have a fever. Please go home", master=root).show()
        except TclError:
            pass
    elif np.max(frame) <= 30.5:
    
                    
        TIME_TO_WAIT = 4000
        root = Tk()
        root.withdraw()
        try:
            root.after(TIME_TO_WAIT, root.destroy)
            Message(title="Error", message="Please move closer to camera and try again", master=root).show()
            
        except TclError:
            pass
        body_temp()
        
    elif np.max(frame) <= 37.5:
          
        TIME_TO_WAIT = 5000
        root = Tk()
        root.withdraw()
        try:
            root.after(TIME_TO_WAIT, root.destroy)
            Message(title="Welcome", message="Your body tempature is ok. Welcome to school", master=root).show()
            
        except TclError:
            pass

        app = App(title="RFID EM4100 Simple GUI", width=350, height=150, layout="auto")
        instructionText = Text(app, text="Click on the text button below\\nand scan your RFid tag.")
        rfidText = TextBox(app)
        rfidStatus = Text(app, text="---")
        checkRFidTag()
        
def plot_update():
            
    fig.canvas.restore_region(ax_background) # restore background
    mlx.getFrame(frame) # read mlx90640
    data_array = np.fliplr(np.reshape(frame,mlx_shape)) # reshape, flip data
    if(imageMirror == 'true'):
        data_array = np.flipud(data_array)
    data_array = ndimage.zoom(data_array,mlx_interp_val) # interpolate
    therm1.set_array(data_array) # set data
    therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
    cbar.on_mappable_changed(therm1) # update colorbar range
    plt.pause(0.001)
    ax.draw_artist(therm1) # draw new thermal image
    textMaxValue.set_text(str(np.round(np.max(data_array), 1)))
    fig.canvas.blit(ax.bbox) # draw background
    fig.canvas.flush_events() # show the new image
    fig.show()
    return
t_array = []
while True:
    t1 = time.monotonic() # for determining frame rate
    t2=time.time()
    try:
        t2=time.time()
        total = t2-t0
        print(total)
        
        if total < 7:
            try:
                plot_update() # update plot
            except:
                continue
        elif total > 12:
            break
        else:
            body_temp()
            break
    except:
        continue
    # approximating frame rate
    t_array.append(time.monotonic()-t1)
    if len(t_array)>10:
        t_array = t_array[1:] # recent times for frame rate approx
    print('Frame Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))





       
        

        

        


