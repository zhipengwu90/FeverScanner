#! /usr/bin/python3
# from gpiozero import LED, Buzzer
from guizero import App, Box, Text, TextBox, warn
import csv
import thermo2 as thermal
#import sys



def clearDisplay():
    print("Clear display")
    rfidStatus.value = "---"
    rfidText.value = ""
    rfidStatus.repeat(1000, checkRFidTag)

def checkRFidTag():
    tagId = rfidText.value
    if tagId != "":
        print("reading nfc")
        RFidRegistered = False
        print(tagId)
        with open("Database.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["RFid"] == tagId:
                    RFidRegistered = True
                    print("Welcome " + row["User"])
                    rfidStatus.value = "Welcome " + row["User"]
                    rfidStatus.after(500, clearDisplay)
                    print("call thermal")
                    thermal.main()
                    
                    
                   

                    
                    
                 
        if RFidRegistered == False:
            print("RFid tag is not registered")
            rfidStatus.value = "RFid tag is not registered"
            rfidStatus.after(3000, clearDisplay)
        
        rfidStatus.cancel(checkRFidTag)

app = App(title="RFID EM4100 Simple GUI", width=550, height=350, layout="auto")

instructionText = Text(app, text="Scan your Student ID.")
rfidText = TextBox(app)
rfidText.focus()
rfidStatus = Text(app, text="---")
rfidStatus.repeat(1000, checkRFidTag)
designBy = Text(app, text="Thermal Scanner", align="bottom")
app.display()


#def click():
 #    time.sleep(0.1)
 #   pyautogui.click()
    
#def main():
 #   for i in range(20)
 #       click()
#main()



if __name__ == "__main__":
    main()
    


