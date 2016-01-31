# Proposal: Rename module to this to prevent naming conflicts
#import serial; FAKE = 0
import fakeSerial as serial; FAKE = 1

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
    #print(x, y)
    return 0
    ser.flushInput()
    ser.write("G%d,%d" % (x, y))
    read = ser.read()
    if read != b'A': print("Warning: Serial did not respond 'Aligned'")
    ser.flushInput()
    ser.write("Q")
    return -int(ser.readline())
    
def getPos():
    return (.5, .5)