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
		root.config(bg = "white")
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
		transmitFrame.config(bg = "white")

		transmitLabel = Label(transmitFrame, text="Transmit", font=("Sans Serif", 20, "bold"), fg="green", bg = "white")
		transmitEntryLabel = Label(transmitFrame, text = "(Instructions for Transmit Input)", font = ("Times New Roman", 9), fg="black", bg = "white")
		transmitEntry = Entry(transmitFrame, width=30, fg="green", highlightthickness = 2, highlightcolor = "green", highlightbackground = "light slate gray")
		transmitButton = Button(transmitFrame, text="SEND", font=("Arial", 8, "bold"), fg="white", bg="green", activebackground = "DarkGreen")

		root.update_idletasks()
		transmitLabel.pack(pady= '10 0')
		transmitEntryLabel.pack(padx = 10, pady = "35 10")
		transmitEntry.pack(padx = 10)
		transmitButton.pack(pady = 10)

		transmitButton.bind('<Transmit_Button>',self.transmit())

	def receiveFrame(self):
		'''Create Receive Canvas and populate with label and entry box'''
		global receiveText

		receiveFrame = Frame(root)
		receiveFrame.grid(column=2, columnspan=2, row=0, rowspan=6)
		receiveFrame.config(bg = "white")

		receiveLabel = Label(receiveFrame, text="Receive", font=("Sans Serif", 20, "bold"), fg="blue", bg = "white")
		receiveText = Text(receiveFrame, width = 30, height = 10, fg = "blue", highlightthickness = 2, highlightcolor = "blue", highlightbackground = "light slate gray")

		root.update_idletasks
		receiveLabel.pack(pady="10 0")
		receiveText.pack(padx = 10, pady = 10)

	def optionsFrame(self):
		'''Create Options Canvas and populate with buttons'''
		optionsFrame = Frame(root)
		optionsFrame.grid(column=0, columnspan=2, row=5)
		optionsFrame.config(bg = "white")

		alignButton = Button(optionsFrame, text="Align", font=("Arial", 8, "bold"), fg = "white", bg = "purple4", activebackground = "purple", command = self.alignButton())
		paramsButton = Button(optionsFrame, text="Set Parameters", font = ("Arial", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan", command = self.paramsButton())

		root.update_idletasks()
		alignButton.grid(column=0, row = 0, padx = 5, pady = "0 10")
		paramsButton.grid(column=1, row = 0, padx = 5, pady = "0 10")

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
		alignWindow.config(bg = "white")
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
		GPSEntryFrame.config(bg = "white")

		GPSLabel = Label(GPSEntryFrame, text="Input GPS coordinates in decimal degrees", font=("Sans Serif", 12, "bold"), bg = "white")
		latitudeField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		longitudeField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		altitudeField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		latitudeLabel = Label(GPSEntryFrame, text="Latitude", font=("Sans Serif", 10, "bold"), bg = "white")
		longitudeLabel = Label(GPSEntryFrame, text="Longitude", font=("Sans Serif", 10, "bold"), bg = "white")
		altitudeLabel = Label(GPSEntryFrame, text = "Altitude", font=("Sans Serif", 10, "bold"), bg = "white")
		GPSButton = Button(GPSEntryFrame, text = "Enter Coordinates", font = ("Sans Serif", 10, "bold"), fg = "white", bg = "purple4", activebackground = "purple")

		GPSLabel.grid(row = 0, column = 0, columnspan = 4, pady  = "10 0")
		latitudeField.grid(row = 1, column = 0, padx = "10 5", pady =  "10 0")
		longitudeField.grid(row = 1, column = 1, padx = 5, pady = "10 0")
		altitudeField.grid(row = 1, column = 2, padx = 5, pady = "10 0")
		GPSButton.grid(row = 1, column = 3, padx = "5 10", pady = "10 0")
		latitudeLabel.grid(row = 2, column = 0)
		longitudeLabel.grid(row = 2, column = 1)
		altitudeLabel.grid(row = 2, column = 2) 

	def addVirtualOscope(self):
		oscopeFrame = Frame(alignWindow)
		oscopeFrame.grid(row=1, column = 0)
		oscopeFrame.config(bg = "white")

		oscopeLabel = Label(oscopeFrame, text = "Photodiode Output", font = ("Sans Serif", 12, "bold"), bg = "white")
		oscopeLabel.pack(pady = 10)
 
	def addControlButtons(self):
		controlButtonsFrame = Frame(alignWindow)
		controlButtonsFrame.grid(row = 2, column = 0)
		controlButtonsFrame.config(bg = "white")

		startButton = Button(controlButtonsFrame, text = "Start", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "DarkGreen", activebackground = "green")
		bigRedButton = Button(controlButtonsFrame, text = "Stop", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "red", activebackground = "orange red")
		closeButton = Button(controlButtonsFrame, text = "Close", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan")
		

		startButton.grid(row = 0, column = 0, pady = "0 10")
		bigRedButton.grid(row = 0, column = 1, padx = 10, pady = "0 10")
		closeButton.grid(row = 0, column = 2, pady = "0 10")

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
		paramsWindow.config(bg = "white")
		self.populateParamsWindow()
		paramsWindow.mainloop()
		# fields: PPM-level, pulse length, sample rate, threshold

	def populateParamsWindow(self):
		self.addParamsFields()
		self.addParamsButtons()

	def addParamsFields(self):
		paramsFieldsFrame = Frame(paramsWindow)
		paramsFieldsFrame.grid(row = 0, column = 0)
		paramsFieldsFrame.config(bg = "white")

		parametersTitle = Label(paramsFieldsFrame, text = "Parameters", font = ("Sans Serif", 12, "bold"), bg = "white")
		ppmLevelLabel = Label(paramsFieldsFrame, text = "PPM-level", font = ("Sans Serif", 10, "bold"), bg = "white")
		pulseLengthLabel = Label(paramsFieldsFrame,  text = "Pulse Length", font = ("Sans Serif", 10, "bold"), bg = "white")
		sampleRateLabel = Label(paramsFieldsFrame, text = "Sample Rate", font = ("Sans Serif", 10, "bold"), bg = "white")
		thresholdLabel = Label(paramsFieldsFrame, text = "Threshold", font = ("Sans Serif", 10, "bold"), bg = "white")

		ppmLevelField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")
		pulseLengthField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")
		sampleRateField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")
		thresholdField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")

		parametersTitle.grid(row = 0, column = 0, columnspan = 2)
		ppmLevelLabel.grid(row = 1, column = 0, padx =  10, pady = "10 5")
		ppmLevelField.grid(row = 1, column = 1, padx = "0 10", pady = "10 5")
		pulseLengthLabel.grid(row = 2, column = 0, padx = 10, pady = 5)
		pulseLengthField.grid(row = 2, column = 1, padx = "0 10", pady =  5)
		sampleRateLabel.grid(row = 3, column = 0, padx = 10, pady = 5)
		sampleRateField.grid(row = 3, column = 1, padx = "0 10", pady = 5)
		thresholdLabel.grid(row = 4, column = 0, padx = 10, pady = "5 10")
		thresholdField.grid(row = 4, column = 1, padx = "0 10", pady = "5 10")

	def addParamsButtons(self):
		paramsButtonsFrame = Frame(paramsWindow)
		paramsButtonsFrame.grid(row = 1, column = 0)
		paramsButtonsFrame.config(bg = "white")

		enterButton = Button(paramsButtonsFrame, text = "Enter", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan")
		cancelButton = Button(paramsButtonsFrame, text = "Cancel", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "red", activebackground = "orange red")

		enterButton.grid(row = 0, column = 0, padx = "0 10", pady = 10)
		cancelButton.grid(row = 0, column = 1, pady = 10)

	def updateParams(self):
		# read from fields and send to encodeDecode.py and hide ParamsWindow
		return 0
