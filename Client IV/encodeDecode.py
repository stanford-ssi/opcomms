"""
encodeDecode.py
Brian Zhang
Functions to bridge the GUI and the parser. 
For sample usage see main()
"""

import zlib
import serialParser
import math
import sys
import struct
import time

""" Returns a 4-byte CRC32 checksum for the given message s"""
def cksum(msg): return struct.pack('I', zlib.crc32(msg))

def send(msg, delay=0): 
    """ Encodes input message and calls the parser method to send it. """
    CHAR_LIMIT = 63
    n_packet = 0
    while msg:
        if len(encode(msg)) <= CHAR_LIMIT:
            n_packet += 1
            sendPacket(msg, n_packet, len(msg))
            return
        old_part = ""
        for i in range(1, len(msg)):
            part = encode(msg[:i])
            if len(part) > CHAR_LIMIT: 
                n_packet += 1
                sendPacket(msg[:i-1], n_packet, i-1)
                if delay: time.sleep(delay)
                break
        msg = msg[i-1:]

def sendPacket(msg, idx, lsent):
    msg = encode(msg)
    print("Sending packet %d (%d encoded to %d bytes): %s" % 
          (idx, lsent, len(msg), str(msg)[2:-1]))
    serialParser.sendMessage(msg)

def encode(msg):
    """ Encodes a message: adds checksum and compresses. Returns result """
    msg = serialParser.toBytes(msg)
    if options["use_cksum"]: msg += cksum(msg)
    if options["compress"]: msg = compress(msg)
    return msg

RCV_FAIL_DECODE = -2
RCV_FAIL_DECOMPRESS = -1
RCV_FAIL_CKSUM = 0
RCV_SUCCESS = 1
RCV_NO_MSG = 2
def receive():
    """ 
    Checks for received message.
    Returns the status, which is one of the following, along with the message.
        RCV_FAIL_DECODE: Could not decode unicode. 
        RCV_FAIL_DECOMPRESS: Message was too garbled to recover.
        RCV_FAIL_CKSUM: Message received but checksum failed.
        RCV_NO_MSG: No message received.
        RCV_SUCCESS: Message received.
    """
    msg = serialParser.checkMessage()
    if msg: status, msg = decode(msg)
    else: status, msg = (RCV_NO_MSG, 0)
    
    if status == RCV_SUCCESS: 
        print("Receive successful")
        print("Message: " + msg)
    elif status == RCV_FAIL_CKSUM:
        print("Checksum failed")
        print("Message: " + msg)
    elif status == RCV_FAIL_DECOMPRESS:
        print("Decompression failed")
    elif status == RCV_FAIL_DECODE:
        print("Decoding failed")
    else: print("No message")        
    return status, msg

def decode(msg):
    """ 
    Decodes a message: decompresses and confirms checksum.
    See receive() for return statuses.
    """
    if options["compress"]:
        try: msg = zlib.decompress(msg)
        except: return RCV_FAIL_DECOMPRESS, 0
    if options["use_cksum"]: msg, ck = msg[:-4], msg[-4:]
    else: ck = cksum(msg) # no check
    try: return ck == cksum(msg), msg.decode()
    except: return RCV_FAIL_DECODE, 0
    
def main():
    # Example: send
    setOptions(use_cksum=1, compress=0)
    while 1:
        line = input("(S)end or (R)eceive?: ").lower()
        if line[0] == 's': 
            msg = input("Enter message: ")
            try:
                with open(msg, "rb") as f:
                    msg = f.read()
            except: pass
            print("Sending message...")
            send(msg)
        # Example: receive, print status and message
        elif line[0] == 'r':
            print("Waiting for recipt of message...")
            status, msg = receive()
            if status == RCV_SUCCESS: 
                print("Receive successful")
                print("Message: " + msg)
            elif status == RCV_FAIL_CKSUM:
                print("Checksum failed")
                print("Message: " + msg)
            elif status == RCV_FAIL_DECOMPRESS:
                print("Decompression failed")
            elif status == RCV_FAIL_DECODE:
                print("Decoding failed")
            else: # status == RCV_NO_MSG
                print("No message...")
        else: print("Invalid. Try again")
        
options = {"use_cksum": 0, "compress": 0}
        
def setOptions(**new_options): 
    """ 
    Allows functions outside this module to set various encode/decode options.
    Possible arguments:
        use_cksum: bool -- whether to attach a checksum to the message
        compress: bool -- whether to compress message
    """
    for arg in new_options:
        if arg in options: 
            options[arg] = new_options[arg]
            print("Option", arg, "set to", new_options[arg])
        else: print("Warning: option " + arg + " does not exist")
        
#---- Utility functions ----#

COMPRESS_LEVEL = 9
""" 
For now these are just wrappers for the zlib functions, which will minimize 
power usage. In the future perhaps we can implement a custom algorithm that 
minimizes transmit time
"""
def compress(msg): return zlib.compress(msg, COMPRESS_LEVEL)
def decompress(msg): return zlib.decompress(msg)

if __name__ == "__main__": main()