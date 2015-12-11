class ClientGUI:
	def __init__(self):
		# creates ClientGUI Window w/ TX box, RX box, buttons
		# put checkMyEmail() in its own thread
		# instantiate an AlignWindow
		# call alignButton() [purpose of this is to force checkMyEmail to block/unblock properly]
		# instantiate a ParamsWindow
		# hide ParamsWindow

	def setMessage(message):
		# prints to receive console

	def transmitButton():
		# blocks checkMyEmail
		# calls send(whatever's in transmit box) method in encodeDecode.py
		# unblocks checkMyEmail

	def alignButton():
		# blocks checkMyEmail
		# unhides alignWindow
		# waits until alignWindow closed
		# unblocks checkMyEmail

	def paramsButton():
		# blocks checkMyEmail
		# unhides paramsWindow
		# waits until paramsWindow closed
		# unblocks checkMyEmail

	def checkMyEmail():
		# runs continuously in another thread after alignWindow hidden:
			# call receive in encodeDecode.py
			# if message found, setMessage(output of encodeDecode.py)


class AlignWindow:
	def __init__(self):
		# target GPS box, "virtual oscilloscope"

	def setGPS():
		# set target GPS locally

	def startButton():
		# send target GPS and alignWindow object to align.py to start alignment procedure
	
	def plot(diodeData):
		# update oscope readout

	def bigRedButton():
		# stop thread in which start() in align.py is running

	def closeButton():
		# hides AlignWindow

	def setFinished():
		# boolean: alignment complete

class ParamsWindow:
	def __init__(self):
		# fields: PPM-level, pulse length, sample rate, threshold

	def updateParams():
		# read from fields and send to encodeDecode.py and hide ParamsWindow


