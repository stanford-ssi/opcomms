import serial
import serial.tools.list_ports as list_ports

ser = None
def setSerial():
    USE_FAKE = -1
    global ser
    if ser: 
        print("Warning: Serial already initialized")
        ser.close()
    ports = [port[0] for port in list_ports.comports()]
    if ports == []:
        try: 
            import fakeSerial
            port = USE_FAKE
            print("No serial port found. Using fake serial...")
        except ImportError: port = ""
    elif len(ports) == 1: 
        print("Port found:", ports[0])
        port = ports[0]
    else: port = input("Please enter a port: ")
    if port == USE_FAKE: ser = fakeSerial.Serial()
    elif port == "": ser = None
    else: ser = serial.Serial(port, 250000)
setSerial()

def sendMessage(msg):
    ser.write(b">" + msg)

def checkMessage():
    ser.flushInput()
    ser.write(b"<")
    print("serialParser: Waiting for serial ready")
    while ser.readline() != b"Waiting for msg:\r\n": pass
    print("serialParser: Waiting for message")
    try: nchar = int(ser.readline())
    except: return b''
    return ser.read(nchar)

def query(x, y):
    ser.flushInput()
    print("\tPos: %d, %d" % (x, y))
    ser.write(b"G%d,%d" % (x, y))
    while ser.readline() == b"Aligned!\r\n": pass
    print("\tAligned")
    avg = sum(signalStr() for i in range(10))
    print("\tStrength:", avg)
    return -avg

def signalStr():
    ser.flushInput()
    ser.write(b"S")
    try: stren = int(ser.readline())
    except: return 0
    #print(stren)
    return stren
    
def getPos():
    ser.flushInput()
    ser.write(b"Z")
    return [int(i) for i in ser.readline().split()]

def moveTo(azi, asc):
    print(azi, asc)
    
def raw(msg): 
    print("Raw command:", msg)
    ser.write(toBytes(msg))
    
def toBytes(inp): 
    """ Converts the input to a bytes-like object if it is not already one. """
    return inp.encode() if isinstance(inp, str) else inp