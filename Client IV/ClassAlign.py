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

global CENTER; CENTER = [0,0];  
global RADIUS; RADIUS = 6.371E6 #Earth radius in meters.
global SER;

global left; left = b"L"
global right; right  = b"R"
global up; up  = b"U"
global down; down = b"D"
global Query; Query = b"Q"
global goto; goto = b"G"
deviceName = '/dev/something'

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
    # def lineSegment(self, move, length, numPoints=20): #move is supposed to be a 0-7 movement signal.
    #     omega = 2; #The two is a weird scaling constant to work in real time.
    #     pauseTime = length/numPoints/omega; 
    #     lineData = [];
    #     Stop();
    #     time.sleep(.3);

    #     moveLeft();

    #     moveLeft();
    #     moveDown();

    #     moveRight();
    #     moveDown();

    #     moveRight();

    #     moveUp();
    #     moveRight();

    #     moveUp();

    #     moveUp();
    #     moveLeft();


    #     for i in range(1,numPoints):
    #         lineData.append(Query());
    #         print(str(lineData[-1]))
    #         time.sleep(pauseTime));
    #         if self.paused or self.killed: return lineData;
    #     Stop();
    #     time.sleep(.3)
    #     return lineData;
    def octogon(self, sigma, numPoints = 100):
        for i in range(0,7):
            lineSegment(i, sigma, int(numPoints/8) );
            # [rasterData.append(lineData) for lineData in (scanTwoLines(azTime, altTime/rows, sampleNum = rowSampleNum))]
    def spiral(self, sigma, numPoints = 100, numRevolutions = 5): #Executes a spiral pattern 
        #and returns [sig, rightAzimuth, Ascension, pointNum] of maximum signal seen by partner
        #For manual setting, use numPoints = 4, numRevolutions = 1;
        #Sigma is the spread factor. The spiral will sweep out within a cone of angle sigma.
        w = 2*3.14159/numPoints*numRevolutions;
        max = 0;
        signalComp = [];
        for t in range(0, numPoints)/numPoints:
            rA = sigma*t*math.cos(w*t) + self.center[0]
            Asc = sigma*t*math.sin(w*t) + self.center[1]
            signal = getPointStrength(rA, Asc) #TODO, stub, 
            singalComp.append = [signal, rA, Asc, t*100]
            if signal>signalComp[max][0]: max = t*100;
            if self.paused or self.killed: return None;
        return signalComp[max]
    def lockOn(self, threshold, initialSpread, repLimit = 10): #An arbitrarily fine alignment system. (Assuming perfect mechanics)
        global CENTER;
        if repLimit < 1: raise Exception("Repeated too many times. Unable to lock"); #Prevents infinite tunneling if you're off course
        maxSig = spiral(initialSpread);
        self.center = [ maxSig[1], maxSig[2] ];
        if self.paused or self.killed: return None;
        if(maxSig[0] < threshold): lockOn(threshold, initialSpread/2, repLimit = repLimit-1 );
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
        print("Left Line Completed") #TODO remove 
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

    def getMax(self,data):
        m =max( [i[-1] for i in data] );
        for i in data:
            if i[-1] is m: return i;


    def autoAlignRec(self,speed, name="_autoAlign.csv", minSpeed = 5, deviation = 6):
        sigma = 2 #scaling factor to make time.sleep() wait for the same amount of time as a rasterScan call.
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
        self.GoTo(self.getMax(rasterData));
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

