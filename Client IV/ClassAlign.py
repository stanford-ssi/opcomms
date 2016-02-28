#Auto-align for the opcomms unit.
#Written by Jake Hillard, copyright 2016, licensed under the MIT open-software license.
#
#For Jake's environment. Don't Delete!
#sudo /home/jake/anaconda3/bin/python ClientGUI.py 


import math
import time
import serial
import serialParser
import csv
import numpy as np

global CENTER; CENTER = [0,0];  
global RADIUS; RADIUS = 6.371E6 #Earth radius in meters.
global SER;

global left; left = b"L"
global right; right  = b"R"
global up; up  = b"U"
global down; down = b"D"
global Query; Query = b"Q"
global goto; goto = b"G"

SER = serialParser.ser

class Align(): #Supposed to be passed by reference somehow.
    def __init__(self):
        self.killed = False
        self.paused = False
        self.left = b"L"
        self.right  = b"R"
        self.up  = b"U"
        self.down = b"D"
        self.query = b"Q"
        self.goto = b"G"
        self.stop = b"X"
        self.goto = b"G"
        self.blink =b"B"
        self.center = [0,0]
        self.stopPause = .5;

    def getGPSAzimuth(self, p1,p2):
        #Returns an Azimuth angle (in radians) for p1 pointing at p2 starting from north.
        #from math notes: u is my position, w is the north dot, and v = you.
        sign = True;
        if(p1[1]>p2[1]): sign = False;
        delta = [p1[0]-p2[0], p1[1]- p2[1]]

        uw = delta[1]
        vw = delta[0]

        uv = math.acos( math.cos(delta[0])*math.cos(delta[1]))
        C = math.acos((math.cos(vw)-math.cos(uv)*math.cos(uw)  )/(  math.sin(uv)*math.sin(uw)))
        if(sign): C= -1*C;
        return C

    def getGPSAscension(self,p1,p2): #Given two lists of GPS points, returns Ascension (in radians) from p1 to p2
        angle = math.atan( (-p1[2]+p2[2])/getDistance(p1, p2));
        return angle

    def getDistance(self,p1,p2):
        return math.sqrt( ((p1[0]-p2[0])*RADIUS)**2 + ((p1[1]-p2[1])*RADIUS)**2 );

    def getPosition(self):
        t = query()
        return [t[0], t[1]]

    def getSensor(self):
        return Query()[2];

    def GoTo(self,p1):
        SER.write(self.goto+ bytes( str(p1[0]) + ',' +str(p1[1]), "UTF-8" )) 
        while True:
            t = SER.readline()
            print(t)
            if "Aligned" in str(t): break
        
    def moveLeft(self):
        SER.write(self.left);

    def moveRight(self):
        SER.write(self.right);

    def moveUp(self):
        SER.write(self.up);

    def moveDown(self):
        SER.write(self.down);
    def Stop(self):
        SER.write(self.stop)
    def setSpeed(self,speed):
        SER.write( bytes( str(speed), "UTF-8"));

    def Query(self):
        SER.flushInput()
        SER.write(self.query)
        recieved = (SER.readline()).decode()
        t = str(recieved).split(" ");
        return [int(t[0].split("'")[-1] ), int(t[1].split("'")[-1]), int( t[2].split("\\")[0] ) ];

    def roughAlign(self,p1,p2):
        global CENTER
        CENTER[0] = getGPSAzimuth(p1,p2);
        CENTER[1] = getGPSAscension(p1,p2);
        reciever.moveAbsolute(CENTER); #TODO, stub, how to actually move
    
    def scanTwoLines(self,azTime, altTime, sampleNum = 100):
        lineData = [];
        self.moveLeft()
        for i in range(1,sampleNum):
            lineData.append(self.Query());
            print(str(lineData[-1]))
            time.sleep(azTime/sampleNum);
            if self.killed: return lineData
        self.Stop();
        time.sleep(self.stopPause);
        self.moveDown();
        print(altTime)
        time.sleep(altTime);
        self.Stop();
        time.sleep(self.stopPause);
        self.moveRight(); #To fix the weird; right then immediatly stop problem we've been facing.
        self.moveRight();
        for i in range(1,sampleNum):
            lineData.append(self.Query());
            print(str(lineData[-1]))
            
            time.sleep(azTime/sampleNum);
            if self.killed: return lineData
        self.Stop();
        time.sleep(self.stopPause);
        return lineData;

    def rasterScan(self,azTime, altTime, rows = 3, rowSampleNum  = 50):
        rasterData = []
        for i in range(1, int(rows)-1):
            print("Hot Pocket Cooked") #TODO remove 
            [rasterData.append(lineData) for lineData in (self.scanTwoLines(azTime, altTime/rows, sampleNum = rowSampleNum))]
            self.moveDown();        
            print("Line Done") #TODO remove 
            time.sleep(altTime/rows);
            self.Stop();
            time.sleep(self.stopPause);
            if self.paused or self.killed: return rasterData
        [rasterData.append(lineData) for lineData in (self.scanTwoLines(azTime, altTime/rows, sampleNum = rowSampleNum))]
        return rasterData

    def writeCSV(self,data, name = "Characterization.csv"):
        with open(name, 'wt') as f:
            writer = csv.writer(f)
            for row in data:
                print("Writing Row:" , row); #TODO remove 
                writer.writerow(row);
        print("Data Written: " + name)


    def getCentroid(self, data, center, radius):
        data = np.array(data)
        pts, wts = data[:, :-1 ], data[:, -1]
        return [int(i) for i in np.average(pts[pts-center < radius], axis= 0, weights = wts[pts-center < radius])]
        #Doesn't deal with overflow. Also, not sure if this is how to effectively handle radius.
        #Also, np arrays make very little sense to me.  
    def getBestPoint(self,data):
        MountResolution = 5;
        window = [max(data[0])-min(data[0], max[data[1]- min[data[1] ]
        center = [int(max(data[0])+min(data[0])) /2), int((max[data[1]-min[data[1]) /2)]
        #Looks at a window of x,y values centered around the center.
        c1 = getCentroid(data, center, window);
        print(c1);
        c2 = getCentroid(data, c1, window/2);
        print(c2);  #iterative Centroids.
        c3 = getCentroid(data, c2, window/4);
        c4 = getCentroid(data, c3, window/8);
        c5 = getCentroid(data, c4, window/16);
        return c5;


        
    def autoAlignRec(self,speed, name="_autoAlign.csv", minSpeed = 5, deviation = 6):
        sigma = 1.3 #scaling factor to make time.sleep() wait for the same amount of time as a rasterScan call.
        self.setSpeed(speed)
        self.Stop();
        time.sleep(self.stopPause);
        self.moveUp()
        self.moveRight()
        time.sleep(deviation*sigma);
        self.Stop();
        time.sleep(self.stopPause);
        rasterData = self.rasterScan(deviation, deviation);
        from pprint import pprint;  #TODO remove 
        pprint(rasterData)
        self.writeCSV(rasterData, name = str(speed) + name);
        self.GoTo(self.getBestPoint(rasterData));
        time.sleep(self.stopPause);
        if speed<= minSpeed: return
        self.autoAlignRec(speed-1, name=name, minSpeed=minSpeed, deviation=deviation);

    def autoAlign(self, speed = 8, minSpeed=5, deviation = 6):
        print("Starting auto align")
        SER.write(b"~");
        self.autoAlignRec(speed, minSpeed = minSpeed, deviation = deviation);
        print("Auto Align Completeeeed!!")
        SER.write(b"~");




#      #Lat      , Long,      ,Alt
# p1 = [37.424928, -122.176934, 100];
# p2 = [37.424157, -122.177866, 150];

# print("Azimuth: " + str(getAzimuth(p1,p2)/3.14159*180));
# print("Ascension: " + str(getAscension(p2,p1)/3.14159*180));

# roughAlign(p1,p2);
# lockOn(threshold, 5*3.14159/180);
if __name__ == '__main__':
    Align().autoAlign()
