from tkinter import *

class MainWindow():
	def __init__(self):
		global root
		# figure out how to put text="OpComms System IV Desktop Client" as the window header
		root = Tk()
		# windowWidth = 800
		# windowHeight = 600
		# root.geometry('{}x{}'.format(windowWidth, windowHeight))
		root.resizable(width=FALSE, height=FALSE)
		self.transmitFrame()
		self.receiveFrame()
		self.optionsFrame()
		root.mainloop()
		
		# global alignWindow
		# global paramsWindow
		# alignWindow = AlignWindow()
		# paramsWindow = ParamsWindow()

		# alignWindow.hide()
		# paramsWindow.hide()

		# put checkMyEmail() in its own thread
		# call alignButton() [purpose of this is to force checkMyEmail to block/unblock properly]

	def transmitFrame(self):
		'''Create Transmit Canvas and populate with label, entry box, and button'''
		global transmitEntry

		transmitFrame = Frame(root)
		transmitFrame.grid(column=0, columnspan=2, row=0, rowspan=3)

		transmitLabel = Label(transmitFrame, text="Transmit", font=("Arial", 20), fg="green")
		transmitEntry = Entry(transmitFrame, width=30, fg="green")
		transmitButton = Button(transmitFrame, text="Send")

		root.update_idletasks()
		transmitLabel.pack()
		transmitEntry.pack()
		transmitButton.pack()

		transmitButton.bind('<Transmit_Button>',self.transmit())

	def receiveFrame(self):
		'''Create Receive Canvas and populate with label and entry box'''
		global receiveText

		receiveFrame = Frame(root)
		receiveFrame.grid(column=2, columnspan=2, row=0, rowspan=6)

		receiveLabel = Label(receiveFrame, text="Receive", font=("Arial", 20), fg="blue")
		receiveText = Text(receiveFrame, width = 30, height = 10, fg = "blue", bd=5)

		root.update_idletasks
		receiveLabel.pack()
		receiveText.pack()

	def optionsFrame(self):
		'''Create Options Canvas and populate with buttons'''
		optionsFrame = Frame(root)
		optionsFrame.grid(column=0, columnspan=2, row=5)

		alignButton = Button(optionsFrame, text="Align", command=self.alignButton())
		paramsButton = Button(optionsFrame, text="Set Parameters")

		root.update_idletasks()
		alignButton.grid(column=0, row = 0)
		paramsButton.grid(column=1, row = 0)

	def setMessage(self, message):
		# prints to receive console
		return 0

	def transmit(self):
		# blocks checkMyEmail
		# calls send(whatever's in transmit box) method in encodeDecode.py
		# unblocks checkMyEmail
		return 0

	def alignButton(self):
		# alignWindow.show()

		# blocks checkMyEmail
		# unhides alignWindow
		# waits until alignWindow closed
		# unblocks checkMyEmail
		return 0;

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


class AlignWindow():
	def __init__(self):
		alignWindow= Tk()
		alignWindow.resizable(width=FALSE, height=FALSE)
		alignWindow.mainloop()

		button = Button(text="Quit", command=alignWindow.destroy)
		button.pack()

		# target GPS box, "virtual oscilloscope"

	def setGPS(self):
		# set target GPS locally
		return 0

	def startButton(self):
		# send target GPS and alignWindow object to align.py to start alignment procedure
		return 0

	def plot(self, diodeData):
		# update oscope readout
		return 0

	def bigRedButton(self):
		# stop thread in which start() in align.py is running
		return 0

	def closeButton(self):
		# hides AlignWindow
		return 0

	def setFinished(self):
		# boolean: alignment complete
		return 0

class ParamsWindow():
	def __init__(self):
		paramsWindow= Tk()
		paramsWindow.resizable(width=FALSE, height=FALSE)
		paramsWindow.mainloop()
		# fields: PPM-level, pulse length, sample rate, threshold

	def updateParams(self):
		# read from fields and send to encodeDecode.py and hide ParamsWindow
		return 0
