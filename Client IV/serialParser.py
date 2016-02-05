import serial
import serial.tools.list_ports as list_ports

ser = None
def setSerial():
    global ser
    if ser: 
        print("Warning: Serial already initialized")
        ser.close()
    ports = [port[0] for port in list_ports.comports()]
    if ports == []:
        try: 
            import fakeSerial
            serial = fakeSerial
            port = ""
            print("No serial port found. Using fake serial...")
        except ImportError:
            raise Exception("Could not open serial port")
    elif len(ports) == 1: 
        print("Port found:", ports[0][0])
        port = ports[0][0]
    else: port = input("Please enter a port: ")
    ser = serial.Serial(port, 250000)
setSerial()

def sendMessage(msg):
    ser.write(b">" + msg)

def checkMessage():
    ser.flushInput()
    ser.write(b"<")
    nchar = ser.read(1)[0]
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

def moveTo(azi, asc):
    print(azi, asc)