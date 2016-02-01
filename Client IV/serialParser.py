# Proposal: Rename module to this to prevent naming conflicts
import serial; FAKE = 0
#import fakeSerial as serial; FAKE = 1

ser = None
def setSerial():
    global ser
    if ser: 
        print("Warning: Serial already initialized")
        ser.close()
    port = "" if FAKE else input("Enter serial port: ")
    ser = serial.Serial(port, 250000)
setSerial()

def sendMessage(msg):
    ser.write(("T%d," % len(msg)).encode() + msg)

def checkMessage():
    ser.flushInput()
    ser.write(b"M")
    nchar = int(ser.readline())
    return ser.read(nchar)

def query(x, y):
    ser.flushInput()
    print("\tPos: %d, %d" % (x, y))
    ser.write(b"G%d,%d" % (x, y))
    line = b""
    while not b"Align" in line:
        line = ser.readline()
        #print(line)
    print("\tAligned")
    avg = sum(signalStr() for i in range(10))
    return -avg

def signalStr():
    ser.flushInput()
    ser.write(b"S")
    int(ser.readline())
    
def getPos():
    ser.flushInput()
    ser.write(b"Q")
    return [int(i) for i in ser.readline().split()[:2]]