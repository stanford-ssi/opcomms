#Characterization unit for a reciever node.
#Designed to have an aligned laser target the reciver, then have the reciever move in a square raster search.
#Hopefully you'll get a list full of

import math
import time
import serial, csv

global SER;

try:
   try:
       SER = serial.Serial('/dev/ttyACM0', baudrate = 250000)  # open serial port
   except:
       SER = serial.Serial('/dev/ttyACM1', baudrate = 250000)  # open serial port
except: raise Exception("Couldn't auto-connect. Are we plugged in?");

print("Teensy connected at " + SER.name)         # check which port was really used



global left; left = b"L"
global right; right  = b"R"
global up; up  = b"U"
global down; down = b"D"
global query; query = b"Q"
global goto; goto = b"G"
global stop; stop = b"X"
global blink; blink =b"B"
global align; align =b"A"

def moveLeft():
    SER.write(left);

def moveRight():
    SER.write(right);

def moveUp():
    SER.write(up);

def moveDown():
    SER.write(down);
def Stop():
    SER.write(stop)
def setSpeed(speed):
    SER.write( bytes( str(speed), "UTF-8"));

def Query():
    SER.flushInput()
    SER.write(query)
    recieved = (SER.readline()).decode()
    t = str(recieved).split(" ");
    return [int(t[0].split("'")[-1] ), int(t[1].split("'")[-1]), int( t[2].split("\\")[0] ) ];


def goPosition(p1):
    SER.write(goto+ bytes( str(p1[0]) + str(p1[1]), "UTF-8" )) 
    while True:
        t = SER.readline()
        print(t)
        if "Aligned" in str(t): break




def scanTwoLines(azTime, altTime, sampleNum = 100):
    lineData = [];
    moveLeft()
    for i in range(1,sampleNum):
        lineData.append(Query());
        print(str(lineData[-1]))
        time.sleep(azTime/sampleNum);
    Stop();
    moveDown();
    print(altTime)
    time.sleep(altTime);
    Stop();
    time.sleep(1)
    moveRight();
    moveRight();
    print("Left Line Completed")
    for i in range(1,sampleNum):
        lineData.append(Query());
        print(str(lineData[-1]))
        
        time.sleep(azTime/sampleNum);
    Stop();
    return lineData;

def rasterScan(azTime, altTime, rows = 6, rowSampleNum  = 75):
    rasterData = []
    for i in range(1, int(rows)-1):
        print("Hot Pocket Cooked")
        [rasterData.append(lineData) for lineData in (scanTwoLines(azTime, altTime/rows, sampleNum = rowSampleNum))]
        moveDown();
        print("Line Done")
        time.sleep(altTime/rows);
        Stop();
        time.sleep(1)
    [rasterData.append(lineData) for lineData in (scanTwoLines(azTime, altTime/rows, sampleNum = rowSampleNum))]
    from pprint import pprint;
    pprint(rasterData)
    writeCSV(rasterData);
    return rasterData

def writeCSV(data, name = "Characterization.csv"):
    with open(name, 'wt') as f:
        writer = csv.writer(f)
        for row in data:
            print("Writing Row:" , row);
            writer.writerow(row);
    print("Data Written")

def getMax(data):
    m =max( [i[-1] for i in data] );
    for i in data:
        if i[-1] is m: return i;


def autoAlignRec(speed, name="Characterization.csv", minSpeed = 5):
    deviation = 6;
    setSpeed(speed)
    moveUp()
    moveRight()
    time.sleep(deviation/3);
    Stop()
    data = getMax(rasterScan(deviation, deviation*2/3, name = "1" + name));
    goPosition(data)
    if speed< minSpeed+1: return
    autoAlign(speed-1, name="1"+name);

def autoAlign(speed, minSpeed=5):
    SER.write(b"~");
    autoAlignRec(speed, minSpeed = minSpeed);


autoAlign(9);


# setSpeed(6)
# SER.write(b"~")
# data =rasterScan(6,4, rows = 6, rowSampleNum = 75)
#m = getMax(data)
# p = m[:2];
# goPosition(p)


