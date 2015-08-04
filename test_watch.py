import os
import sys
import time
import threading
import Image
import ImageDraw
from Adafruit_LED_Backpack import Matrix8x8

""" This class uses threading.Thread to inherit from.
The class will read the average load and write it to
std out and to an 8x8 matrix display. """
class LoadThread(threading.Thread):
    """ Init takes in the default stopcondition and 
        the target display matrix """
    def __init__(self, stopcond, matrixdisplay):
        super(LoadThread,self).__init__()
        self.stopcond = False
        self.display = matrixdisplay
        self.image = Image.new('1',(8,8))
    

    """ Create Idle Image """
    def createImage(self):
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((0,0,7,7),outline=255, fill=0)
        draw.line((2,2,5,2),fill=255)
        draw.line((2,5,5,5),fill=255)
        draw.rectangle((3,3,4,4),fill=255)


    """ Run method which loops until the stopcondition
        is set. It will read the average load of the system
        and call writeMinute to write out information."""

    def run(self):
        self.createImage()
        while not self.stopcond:
	    av1, av2, av3 = os.getloadavg()
            #print " Load average: %.2f %.2f %.2f " % (av1, av2, av3)
            self.writeMinute(av1)
            time.sleep(1)

    """ This will take an float average load value and scale it to 
        fit on a 8x8 matrix which will fill in rows until full. """
    def writeMinute(self,averageLoad):
        loadVal = int(round(averageLoad * 16.0))
        print loadVal
        if loadVal > 0:
            display.clear()
            current = 1;
            for x in range(8):
                for y in range(7,-1,-1):
                    if current <= loadVal:
                        display.set_pixel(x,y,1)
                    current = current + 1
	    display.write_display()
        else:
            display.clear()
            display.set_image(self.image)
            display.write_display()

            


    """ Called to stop the thread by setting stopcond to true."""
    def stopthread(self):
        self.stopcond = True
    

if __name__ == "__main__":
    #Initialise Display and thread.
    display = Matrix8x8.Matrix8x8()
    display.clear()
    display.write_display()
    thread_watch = LoadThread(False, display) 
    thread_watch.start()
    try: #Loop until keyboard interrupt
       while True:
           time.sleep(1)
    except KeyboardInterrupt:
       thread_watch.stopthread()
    thread_watch.join()
    #Clear display
    display.clear()
    display.write_display()
