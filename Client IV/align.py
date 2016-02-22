#Auto-align for the opcomms unit.
#Written by Jake Hillard, copyright 2016, licensed under the MIT open-software license.
#
#Assumptions:
#=============
#   *GPS coordinates are given as [lat, long, altitude]
#   *We can easily get lots of data from NodeB to NodeA without having an optical lock.
#
#
#Stubs that still need to be fleshed out:
#========================================
#    *reciever.moveAbsolute(rightAzimuth, Ascension) given exact coordinates, move to to angle.
#    *WifiLink.getPartnerSensor(); Get the current voltage of the sensor
#    *laser.On() & laser.Off() Turning the laser on and off. 

import math
import time
import serial
import serialParser

global CENTER; CENTER = [0,0];
global RADIUS; RADIUS = 6.371E6 #Earth radius in meters.
global SER;


global left; left = b"L"
global right; right  = b"R"
global up; up  = b"U"
global down; down = b"D"
global query; query = b"Q"
global goto; goto = b"G"
global stop; stop = b"X"
global blink; blink =b"B"
global align; align =b"A"


deviceName = '/dev/something'

SER = serialParser.ser

#2^24-1 is a full rev
#Write the full move to GPS coord. Check.
#Write the full auto align.
#Draw up the new signal Board.

def getGPSAzimuth(p1,p2):
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

def getGPSAscension(p1,p2): #Given two lists of GPS points, returns Ascension (in radians) from p1 to p2
    angle = math.atan( (-p1[2]+p2[2])/getDistance(p1, p2));
    return angle

def alignGPS(p1,p2):
	#Gives you a difference in 2^24-1 armians.
	pi = 3.14159;
	az = getGPSAzimuth(p1,p2);
	alt = getGPSAscension(p1,p2);
	SER.write(b"A" + str(az/(2*pi)*(2^24-1)) + "," + str(alt/(2*pi)*(2^24-1)));



	#Stub; get gps angles and add the things.

def getDistance(p1,p2):
    return math.sqrt( ((p1[0]-p2[0])*RADIUS)**2 + ((p1[1]-p2[1])*RADIUS)**2 );

def getPosition():
    t = query()
    return [t[0], t[1]]



def getSensor():
    SER.flushInput()
    SER.write(query)
    temp = SER.readline()
    return str(temp).split(" ")[-1].split("\\")[0]

def goPosition(p1):
    SER.write(goto+ bytes( str(p1[0]) + str(p1[1]), "UTF-8" )) 
    while True:
        t = SER.readline()
        print(t)
        if "Aligned" in str(t): break
    

def getPointStrength(rightAzimuth, Ascension): #All kinds of assumptions being made here
    reciever.moveAbsolute(rightAzimuth, Ascension) #Assumes coordinates are absolute
    laser.on();
    #sig = input("Manual Signal Strength: ");
    sig = wifiLink.getPartnerSensor();
    laser.off();
    return si


def moveLeft():
    SER.write(left);

def moveRight():
    SER.write(right);

def moveUp():
    SER.write(up);

def moveDown():
    SER.write(down);

 

def query():
    SER.flushInput()
    SER.write(Query)
    recieved = SER.readline()
    t = str(recieved).split(" ");
    return [int(t[0].split("'")[-1] ), int(t[1].split("'")[-1]), int( t[-1].split("\\")[0] ) ];

def stop():
    SER.write(b"X")

def recieverCrossOptimize():
    global SER;
    signalStrength = 0
    Azimuth = 0;
    Ascension = 0;
    

    delay = 0.05; 
    maxSig = [0, 0, 0];
    numBytes = 4;
       #Sig Strength, Azimuth, Ascension
    
    moveLeft();
    for i in range (1,50):
        currSig = query();
        if currSig[2] > maxSig[2]: maxSig = currSig[:];
        print(currSig[2]) 
        time.sleep(delay)
    moveRight();
    for i in range (1,100):
        currSig = query();
        if currSig[2] > maxSig[2]: maxSig = currSig[:];
        print(currSig[2]) 
        time.sleep(delay)

    goPosition( [ maxSig[0], maxSig[1]] );
    
    moveUp();
    for i in range (1,25):
        currSig = query();
        if currSig[2] > maxSig[2]: maxSig = currSig[:]; 
        print(currSig[2])
        time.sleep(delay)
    moveDown();
    for i in range (1,50):
        currSig = query();
        if currSig[2] > maxSig[2]: maxSig = currSig[:]; 
        print(currSig[2])
        time.sleep(delay)

    goPosition( [maxSig[0], maxSig[1]] );






def spiral(sigma, numPoints = 100, numRevolutions = 5): #Executes a spiral pattern 
    #and returns [sig, rightAzimuth, Ascension, pointNum] of maximum signal seen by partner
    #For manual setting, use numPoints = 4, numRevolutions = 1;
    #Sigma is the spread factor. The spiral will sweep out within a cone of angle sigma.
    sigma = sigma/2; #Accounts for the fact that we are rotating about angle CENTER.
    w = 2*3.14159/numPoints*numRevolutions;
    max = 0;
    signalComp = [];
    for t in range(0, numPoints)/numPoints:
        rA = sigma*t*math.cos(w*t) + CENTER[0]
        Asc = sigma*t*math.sin(w*t) + CENTER[1]
        signal = getPointStrength(rA, Asc) #TODO, stub, 
        singalComp.append = [signal, rA, Asc, t*100]
        if signal>signalComp[max][0]: max = t*100;
    return signalComp[max]

def lockOn(threshold, initialSpread, repLimit = 10): #An arbitrarily fine alignment system. (Assuming perfect mechanics)
    global CENTER;
    if repLimit < 1: raise Exception("Repeated too many times. Unable to lock"); #Prevents infinite tunneling if you're off course
    maxSig = spiral(initialSpread);
    CENTER = [ maxSig[1], maxSig[2] ];
    if(maxSig[0] < threshold): lockOn(threshold, initialSpread/2, repLimit = repLimit-1 );


def roughAlign(p1,p2):
    global CENTER
    CENTER[0] = getGPSAzimuth(p1,p2);
    CENTER[1] = getGPSAscension(p1,p2);
    reciever.moveAbsolute(CENTER); #TODO, stub, how to actually move
SER.write(b"7")



#      #Lat      , Long,      ,Alt
# p1 = [37.424928, -122.176934, 100];
# p2 = [37.424157, -122.177866, 150];

# print("Azimuth: " + str(getAzimuth(p1,p2)/3.14159*180));
# print("Ascension: " + str(getAscension(p2,p1)/3.14159*180));

# roughAlign(p1,p2);
# lockOn(threshold, 5*3.14159/180);

