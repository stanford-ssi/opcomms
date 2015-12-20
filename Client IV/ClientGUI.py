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

		 #put checkMyEmail() in its own thread
		 #call alignButton() [purpose of this is to force checkMyEmail to block/unblock properly]

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
		global alignWindow
		alignWindow= Tk()
		alignWindow.resizable(width=FALSE, height=FALSE)
		self.populateAlignWindow()
		alignWindow.mainloop()


		# target GPS box, "virtual oscilloscope"
	def populateAlignWindow(self):
		self.addGPSEntry()
		self.addVirtualOscope()
		self.addControlButtons()

	def addGPSEntry(self):
		GPSEntryFrame = Frame(alignWindow)
		GPSEntryFrame.grid(row = 0, column = 0)
		latitudeField = Entry(GPSEntryFrame)
		longitudeField = Entry(GPSEntryFrame)
		altitudeField = Entry(GPSEntryFrame)
		GPSLabel = Label(GPSEntryFrame, text="Input GPS coordinates in decimal degrees")
		latitudeLabel = Label(GPSEntryFrame, text="Latitude")
		longitudeLabel = Label(GPSEntryFrame, text="Longitude")
		altitudeLabel = Label(GPSEntryFrame, text = "Altitude")
		GPSButton = Button(GPSEntryFrame, text = "Enter Coordinates")

		GPSLabel.grid(row = 0, column = 0, columnspan = 4)
		latitudeField.grid(row = 1, column = 0)
		longitudeField.grid(row = 1, column = 1)
		altitudeField.grid(row = 1, column = 2)
		GPSButton.grid(row = 1, column = 3)
		latitudeLabel.grid(row = 2, column = 0)
		longitudeLabel.grid(row = 2, column = 1)
		altitudeLabel.grid(row = 2, column = 2)

	def addVirtualOscope(self):
		oscopeFrame = Frame(alignWindow)
		oscopeFrame.grid(row=1, column = 0)
		oscopeLabel = Label(oscopeFrame, text = "Photodiode Output")
		oscopeLabel.pack()

	def addControlButtons(self):
		controlButtonsFrame = Frame(alignWindow)
		controlButtonsFrame.grid(row = 2, column = 0)
		startButton = Button(controlButtonsFrame, text = "Start")
		closeButton = Button(controlButtonsFrame, text = "Close")
		bigRedButton = Button(controlButtonsFrame, text = "Stop")

		startButton.grid(row = 0, column = 0)
		bigRedButton.grid(row = 0, column = 1)
		closeButton.grid(row = 0, column = 2)

	def setGPS(self):
		# set target GPS locally
		return 0

	def start(self):
		# send target GPS and alignWindow object to align.py to start alignment procedure
		return 0

	def plot(self, diodeData):
		# update oscope readout
		return 0

	def stop(self):
		# stop thread in which start() in align.py is running
		return 0

	def close(self):
		# hides AlignWindow
		return 0

	def setFinished(self):
		# boolean: alignment complete
		return 0

class ParamsWindow():
	def __init__(self):
		global paramsWindow
		paramsWindow= Tk()
		paramsWindow.resizable(width=FALSE, height=FALSE)
		self.populateParamsWindow()
		paramsWindow.mainloop()
		# fields: PPM-level, pulse length, sample rate, threshold

	def populateParamsWindow(self):
		self.addParamsFields()
		self.addParamsButtons()

	def addParamsFields(self):
		paramsFieldsFrame = Frame(paramsWindow)
		paramsFieldsFrame.grid(row = 0, column = 0)

		parametersTitle = Label(paramsFieldsFrame, text = "Parameters")
		ppmLevelLabel = Label(paramsFieldsFrame, text = "PPM-level")
		pulseLengthLabel = Label(paramsFieldsFrame,  text = "Pulse Length")
		sampleRateLabel = Label(paramsFieldsFrame, text = "Sample Rate")
		thresholdLabel = Label(paramsFieldsFrame, text = "Threshold")

		ppmLevelField = Entry(paramsFieldsFrame)
		pulseLengthField = Entry(paramsFieldsFrame)
		sampleRateField = Entry(paramsFieldsFrame)
		thresholdField = Entry(paramsFieldsFrame)

		parametersTitle.grid(row = 0, column = 0, columnspan = 2)
		ppmLevelLabel.grid(row = 1, column = 0)
		ppmLevelField.grid(row = 1, column = 1)
		pulseLengthLabel.grid(row = 2, column = 0)
		pulseLengthField.grid(row = 2, column = 1)
		sampleRateLabel.grid(row = 3, column = 0)
		sampleRateField.grid(row = 3, column = 1)
		thresholdLabel.grid(row = 4, column = 0)
		thresholdField.grid(row = 4, column = 1)

	def addParamsButtons(self):
		paramsButtonsFrame = Frame(paramsWindow)
		paramsButtonsFrame.grid(row = 1, column = 0)

		enterButton = Button(paramsButtonsFrame, text = "Enter")
		cancelButton = Button(paramsButtonsFrame, text = "Cancel")

		enterButton.grid(row = 0, column = 0)
		cancelButton.grid(row = 0, column = 1)

	def updateParams(self):
		# read from fields and send to encodeDecode.py and hide ParamsWindow
		return 0
