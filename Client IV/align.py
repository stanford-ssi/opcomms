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

global CENTER;
global RADIUS;
RADIUS = 6.371E6 #Earth radius in meters.
CENTER = [0,0];

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

def getDistance(p1,p2):
    return math.sqrt( ((p1[0]-p2[0])*RADIUS)**2 + ((p1[1]-p2[1])*RADIUS)**2 );

def getPointStrength(rightAzimuth, Ascension): #All kinds of assumptions being made here
    reciever.moveAbsolute(rightAzimuth, Ascension) #Assumes coordinates are absolute
    laser.on();
    sig = wifiLink.getPartnerSensor();
    laser.off();
    return si

def spiral(sigma, numPoints = 100, numRevolutions = 5): #Executes a spiral pattern  
                       #and returns [sig, rightAzimuth, Ascension, pointNum] of maximum signal seen by partner
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




     #Lat      , Long,      ,Alt
p1 = [37.424928, -122.176934, 100];
p2 = [37.424157, -122.177866, 150];

print("Azimuth: " + str(getAzimuth(p1,p2)/3.14159*180));
print("Ascension: " + str(getAscension(p2,p1)/3.14159*180));

roughAlign(p1,p2);
lockOn(threshold, 5*3.14159/180);
