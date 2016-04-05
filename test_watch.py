import os
import sys
import time
import threading
import Image
import ImageDraw
import psutil
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
        self.images = {0:Image.new('1',(8,8)),1:Image.new('1',(8,8))}
        self.current = 0;
        self.metric = 0

    

    """ Create Idle Image """
    def createImage(self):
        draw = ImageDraw.Draw(self.images[self.current])
        #draw.rectangle((0,0,7,7),outline=255, fill=0)
        draw.line((1,1,6,1),fill=255)
        draw.line((1,6,6,6),fill=255)
        draw.rectangle((3,2,4,5),fill=255)
        self.current = not self.current
        draw = ImageDraw.Draw(self.images[self.current])
        #draw.rectangle((0,0,7,7),outline=255, fill=0)
        draw.line((1,1,1,6),fill=255)
        draw.line((6,1,6,6),fill=255)
        draw.rectangle((2,3,5,4),fill=255)

    """ Run method which loops until the stopcondition
        is set. It will read the average load of the system
        and call writeMinute to write out information."""

    def updateMetric(self):
        print os.path.exists("metric.txt")
        if os.path.exists("metric.txt"):
           file=open("metric.txt")
           temp = int(file.read())
           self.metric = temp
           #print self.metric
           file.close()
          
    def run(self):
        self.createImage()
        loop = 1;
        while not self.stopcond:
            print loop
            if loop % 20 == 0: 
                self.updateMetric()
                loop = 0
	    #av1, av2, av3 = os.getloadavg()
            if self.metric == 0:
                cpupercent = psutil.cpu_percent(interval=1,percpu=True)
                self.writeCpus(cpupercent)
            if self.metric == 1:
                av1, av2, av3 = os.getloadavg()
                self.writeMinute(av1)
                time.sleep(1)
            #print " Load average: %.2f %.2f %.2f " % (av1, av2, av3)
            loop = loop + 1
            #time.sleep(1)

    """ This will take an float average load value and scale it to 
        fit on a 8x8 matrix which will fill in rows until full. """
    def writeCpus(self,cpupercent):
        
        cpus = len(cpupercent)
        width = 8/cpus
        perVal = [int(round(x*8.0/100.0)) for x in cpupercent]
        #print loadVal
        self.display.clear()
        bars = Image.new('1',(8,8))
        draw = ImageDraw.Draw(bars)
        #print cpupercent
        #print perVal
        for cpu in range(cpus):
             draw = ImageDraw.Draw(bars)
             if perVal[cpu] > 0:
                draw.line((0+(width*cpu),7,0+(width*cpu),8-perVal[cpu]),fill=255)
                draw.line((1+(width*cpu),7,1+(width*cpu),8-perVal[cpu]),fill=255)
             else:
                draw.line((0+(width*cpu),7,0+(width*cpu),8-perVal[cpu]),fill=0)
                draw.line((1+(width*cpu),7,1+(width*cpu),8-perVal[cpu]),fill=0)
        self.display.set_image(bars)
        self.display.write_display()


    """ This will take an float average load value and scale it to 
        fit on a 8x8 matrix which will fill in rows until full. """
    def writeMinute(self,averageLoad):
        loadVal = int(round(averageLoad * 16.0))
        #print loadVal
        if loadVal > 0:
            self.display.clear()
            current = 1;
            for x in range(8):
                for y in range(7,-1,-1):
                    if current <= loadVal:
                        self.display.set_pixel(x,y,1)
                    current = current + 1
	    self.display.write_display()
        else:
            self.display.clear()
            self.display.set_image(self.images[self.current])
            self.current = not self.current
            self.display.write_display()

            


    """ Called to stop the thread by setting stopcond to true."""
    def stopthread(self):
        self.stopcond = True

    

     
if __name__ == "__main__":
    #Initialise Display and thread.
    displays = Matrix8x8.Matrix8x8()
    displays.begin()
    displays.clear()
    displays.write_display()
    thread_watch = LoadThread(False, displays)
    thread_watch.start()
    try: #Loop until keyboard interrupt
       while True:
           time.sleep(1)
    except (KeyboardInterrupt,SystemExit):
       thread_watch.stopthread()
    thread_watch.join()
    #Clear display
    displays.clear()
    displays.write_display()

