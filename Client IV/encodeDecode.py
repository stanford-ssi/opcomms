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

def send(msg): 
    """ Encodes input message and calls the parser method to send it. """
    serialParser.sendMessage(encode(msg))

def encode(msg):
    """ Encodes a message: adds checksum and compresses. Returns result """
    msg = toBytes(msg)
    msg += bytes([hash(msg) % 256])
    msg = compress(msg)
    return msg

RCV_NO_MSG = -2
RCV_FAIL_DECOMPRESS = -1
RCV_FAIL_CKSUM = 0
RCV_SUCCESS = 1
def receive():
    """ 
    Checks for received message.
    Returns the status, which is one of the following, along with the message.
        RCV_NO_MSG: No message received.
        RCV_FAIL_DECOMPRESS: Message was too garbled to recover.
        RCV_FAIL_CKSUM: Message received but checksum failed.
        RCV_SUCCESS: Message received, checksum confirmed.
    """
    msg = serialParser.checkMessage()
    if msg: return decode(msg)
    else: return RCV_NO_MSG, 0

def decode(msg):
    """ 
    Decodes a message: decompresses and confirms checksum.
    See receive() for return statuses.
    """
    try: msg = zlib.decompress(msg)
    except: return RCV_FAIL_DECOMPRESS, 0
    msg, cksum = msg[:-1], msg[-1]
    return cksum == hash(msg) % 256, msg.decode()
    
def main():
    # Example: send
    send("testing")
    # Example: receive, print status and message
    status, msg = receive()
    if status == RCV_SUCCESS: 
        print("Checksum confirmed")
        print("Message: " + msg)
    elif status == RCV_FAIL_CKSUM:
        print("Checksum failed")
        print("Message: " + msg)
    elif status == RCV_FAIL_DECOMPRESS:
        print("Decompression failed")
    else: # status == RCV_NO_MSG
        print("No message...")
        
#---- Utility functions ----#

COMPRESS_LEVEL = 9
""" 
For now these are just wrappers for the zlib functions, which will minimize 
power usage. In the future perhaps we can implement a custom algorithm that 
minimizes transmit time
"""
def compress(msg): return zlib.compress(msg, COMPRESS_LEVEL)
def decompress(msg): return zlib.decompress(msg)
    
def toBytes(inp): 
    """ Converts the input to a bytes-like object if it is not already one. """
    return inp.encode() if isinstance(inp, str) else inp

if __name__ == "__main__": main()