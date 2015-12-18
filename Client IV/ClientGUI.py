from tkinter import *

class MainWindow():
	def __init__(self):
		global root
		root = Tk()
		# windowWidth = 800
		# windowHeight = 600
		# root.geometry('{}x{}'.format(windowWidth, windowHeight))
		root.resizable(width=FALSE, height=FALSE)
		self.transmitCanvas()
		self.receiveCanvas()
		self.optionsCanvas()
		root.mainloop()
		# creates ClientGUI Window w/ TX box, RX box, buttons
		# put checkMyEmail() in its own thread
		# instantiate an AlignWindow
		# call alignButton() [purpose of this is to force checkMyEmail to block/unblock properly]
		# instantiate a ParamsWindow
		# hide ParamsWindow

	def transmitCanvas(self):
		'''Create Transmit Canvas and populate with label, entry box, and button'''
		transmitCanvas = Canvas(root)
		transmitCanvas.grid(column=0, columnspan=2, row=0, rowspan=5)

		transmitLabel = Label(transmitCanvas, text="Transmit", font=("Arial", 20), fg="green")
		transmitEntry = Entry(transmitCanvas)
		transmitButton = Button(transmitCanvas, text="Enter Transmission")

		root.update_idletasks()
		transmitLabel.pack()
		transmitEntry.pack()
		transmitButton.pack()

		transmitButton.bind('<Transmit_Button>',self.transmit())

	def receiveCanvas(self):
		'''Create Receive Canvas and populate with label and entry box'''
		receiveCanvas = Canvas(root)
		receiveCanvas.grid(column=2, columnspan=2, row=0, rowspan=6)

		receiveLabel = Label(receiveCanvas, text="Receive", font=("Arial", 20), fg="blue")
		receiveText = Text(receiveCanvas, height=10)

		root.update_idletasks
		receiveLabel.pack()
		receiveText.pack()

	def optionsCanvas(self):
		'''Create Options Canvas and populate with buttons'''
		receiveCanvas = Canvas(root)
		receiveCanvas.grid(column=0, columnspan=2, row=5)

	def setMessage(self, message):
		# prints to receive console
		return 0

	def transmit(self):
		# blocks checkMyEmail
		# calls send(whatever's in transmit box) method in encodeDecode.py
		# unblocks checkMyEmail
		return 0

	def alignButton(self):
		# blocks checkMyEmail
		# unhides alignWindow
		# waits until alignWindow closed
		# unblocks checkMyEmail
		return 0

	def paramsButton(self):
		# blocks checkMyEmail
		# unhides paramsWindow
		# waits until paramsWindow closed
		# unblocks checkMyEmail
		return 0

	def checkMyEmail(self):
		# runs continuously in another thread after alignWindow hidden:
			# call receive in encodeDecode.py
			# if message found, setMessage(output of encodeDecode.py)
			return 0


# class AlignWindow():
# 	def __init__(self):
# 		# target GPS box, "virtual oscilloscope"

# 	def setGPS(self):
# 		# set target GPS locally

# 	def startButton(self):
# 		# send target GPS and alignWindow object to align.py to start alignment procedure
	
# 	def plot(self, diodeData):
# 		# update oscope readout

# 	def bigRedButton(self):
# 		# stop thread in which start() in align.py is running

# 	def closeButton(self):
# 		# hides AlignWindow

# 	def setFinished(self):
# 		# boolean: alignment complete

# class ParamsWindow(self):
# 	def __init__(self):
# 		# fields: PPM-level, pulse length, sample rate, threshold

# 	def updateParams(self):
# 		# read from fields and send to encodeDecode.py and hide ParamsWindow


