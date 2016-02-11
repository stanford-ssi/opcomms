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
global query; query = b"Q"
global goto; goto = b"G"
global stop; stop = b"X"
global blink; blink =b"B"

try:
   try:
       SER = serial.Serial('/dev/ttyACM0', baudrate = 250000)  # open serial port
   except:
       SER = serial.Serial('/dev/ttyACM1', baudrate = 250000)  # open serial port
except: raise Exception("Couldn't auto-connect. Are we plugged in?");

print("Teensy connected at " + SER.name)         # check which port was really used

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




def scanTwoLines(azTime, altTime, sampleNum = 100):
    lineData = [];
    moveLeft()
    for i in range(1,sampleNum):
        lineData.append(Query());
        print("waiting for: " + str(azTime/sampleNum) + " : " + str(i));
        time.sleep(azTime/sampleNum);
    Stop();
    moveDown();
    print(altTime)
    time.sleep(altTime);
    Stop();
    time.sleep(1)
    moveRight();
    moveRight();
    print("why am I not moving?")
    for i in range(1,sampleNum):
        lineData.append(Query());
        print(str(lineData[-1]))
        time.sleep(azTime/sampleNum);
    Stop();
    return lineData;

def rasterScan(azTime, altTime, rows = 10, rowSampleNum  = 100):

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

def writeCSV(data):
	with open('AcceptanceCharacterization.csv', 'wt') as f:
		writer = csv.writer(f)
		for row in data:
			writer.writerow(row)

lolWut = []
for i in range(1,10):
    lolWut.append([1,2,3])
writeCSV(lolWut);
# rasterScan(1, 1);
   
