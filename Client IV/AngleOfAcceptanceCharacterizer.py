#Characterization unit for a reciever node.
#Designed to have an aligned laser target the reciver, then have the reciever move in a square raster search.
#Hopefully you'll get a list full of

import math
import time
import serial, csv

global SER;

global left; left = b"L"
global right; right  = b"R"
global up; up  = b"U"
global down; down = b"D"
global Query; Query = b"Q"
global goto; goto = b"G"
global stop; stop = b"X"
global blink; blink =b"B"

#try:
#    try:
#        SER = serial.Serial('/dev/ttyACM1', baudrate = 250000)  # open serial port
#    except:
#        SER = serial.Serial('/dev/ttyACM0', baudrate = 250000)  # open serial port
#except: raise Exception("Couldn't auto-connect. Are we plugged in?");

#print("Teensy connected at " + SER.name)         # check which port was really used

def moveLeft():
    SER.write(left);

def moveRight():
    SER.write(right);

def moveUp():
    SER.write(up);

def moveDown():
    SER.write(down);
def stop():
    SER.write(stop)
def setSpeed(speed):
    SER.write( bytes( str(speed), "UTF-8"));

def query():
    SER.flushInput()
    SER.write(Query)
    recieved = SER.readline()
    t = str(recieved).split(" ");
    return [int(t[0].split("'")[-1] ), int(t[1].split("'")[-1]), int( t[-1].split("\\")[0] ) ];




def scanTwoLines(azTime, altTime, sampleNum = 100):
    lineData = [];
    moveLeft()
    for i in range(1,sampleNum):
        lineData.append(query());
        time.sleep(azTime/sampleNum);
    stop();
    moveDown();
    time.sleep(altTime);
    stop();
    moveRight();
    for i in range(1,sampleNum):
        lineData.append(query());
        time.sleep(azTime/sampleNum);
    stop();
    return lineData;

def rasterScan(azTime, altTime, rows = 10, rowSampleNum  = 100):
    rows = rows/2;
    rasterData = []
    for i in range(1, rows-1):
        rasterData.append(scanTwoLines(azTime, altTime/rows, sampleNum = rowSampleNum))
        moveDown();
        time.sleep(altTime);
        stop();
    scanTwoLines(azTime, altTime/rows, sampleNum = rowSampleNum)
    writeCSV(rasterData);

def writeCSV(data):
	with open('AcceptanceCharacterization.csv', 'wt') as f:
		writer = csv.writer(f)
		for row in data:
			writer.writerow(row)

data = []
for i in range(1,5):
	data. append(["asdas", 56]);
writeCSV(data)
    
