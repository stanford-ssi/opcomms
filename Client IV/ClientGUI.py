from tkinter import *
from threading import *
from time import *

# To Do (Elizabeth):
	# initialize Toplevel in terms of self (not root)

class MainWindow(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
		# windowWidth = 800
		# windowHeight = 600
		# self.geometry('{}x{}'.format(windowWidth, windowHeight))
		self.resizable(width=FALSE, height=FALSE)
		self.config(bg = "white")
		self.transmitFrame()
		self.receiveFrame()
		self.optionsFrame()
		self.update_idletasks()
		self.receiveText.insert(END, "Hello!")

		self.align = AlignWindow(self)
		self.align.window.title("Align Node")
		self.align.window.withdraw()

		self.params = ParamsWindow(self)
		self.params.window.title("Set PPM Parameters")
		self.params.window.withdraw()

		#self.messageChecker = MessageThread(1, "Thread-1", self)
		#self.messageChecker.start()
		self.openAlign()

	def transmitFrame(self):
		'''Create Transmit Canvas and populate with label, entry box, and button'''

		transmitFrame = Frame(self)
		transmitFrame.grid(column=0, columnspan=2, row=0, rowspan=3)
		transmitFrame.config(bg = "white")

		transmitLabel = Label(transmitFrame, text="Transmit", font=("Sans Serif", 20, "bold"), fg="#006400", bg = "white")
		transmitEntryLabel = Label(transmitFrame, text = "(Instructions for Transmit Input)", font = ("Times New Roman", 9), fg="black", bg = "white")
		self.transmitEntry = Entry(transmitFrame, width=30, fg="green", highlightthickness = 2, highlightcolor = "green", highlightbackground = "light slate gray")
		transmitButton = Button(transmitFrame, text="SEND", font=("Arial", 8, "bold"), fg="white", bg="green", activebackground = "DarkGreen", command=self.transmit)

		transmitLabel.pack(pady= '10 0')
		transmitEntryLabel.pack(padx = 10, pady = "35 10")
		self.transmitEntry.pack(padx = 10)
		transmitButton.pack(pady = 10)

	def receiveFrame(self):
		'''Create Receive Canvas and populate with label and entry box'''
		receiveFrame = Frame(self)
		receiveFrame.grid(column=2, columnspan=2, row=0, rowspan=6)
		receiveFrame.config(bg = "white")

		receiveLabel = Label(receiveFrame, text="Receive", font=("Sans Serif", 20, "bold"), fg="blue", bg = "white")
		self.receiveText = Text(receiveFrame, width = 30, height = 10, fg = "blue", highlightthickness = 2, highlightcolor = "blue", highlightbackground = "light slate gray")

		receiveLabel.pack(pady="10 0")
		self.receiveText.pack(padx = 10, pady = 10)

	def optionsFrame(self):
		'''Create Options Canvas and populate with buttons'''
		optionsFrame = Frame(self)
		optionsFrame.grid(column=0, columnspan=2, row=5)
		optionsFrame.config(bg = "white")

		alignButton = Button(optionsFrame, text="Align", font=("Arial", 8, "bold"), fg = "white", bg = "purple4", activebackground = "purple", command = self.openAlign)
		paramsButton = Button(optionsFrame, text="Set Parameters", font = ("Arial", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan", command = self.openParams)

		alignButton.grid(column=0, row = 0, padx = 5, pady = "0 10")
		paramsButton.grid(column=1, row = 0, padx = 5, pady = "0 10")

	def transmit(self):
		#self.messageChecker.paused = True
		# calls send(whatever's in transmit box) method in encodeDecode.py
		#self.messageChecker.paused = False

		return 0

	def openAlign(self):
		#self.messageChecker.paused = True
		self.align.window.deiconify()

		#while not self.align.window.state() == "withdrawn":
		#	sleep(0.001)
		
		#self.messageChecker.paused = False

	def openParams(self):
		#self.messageChecker.paused = True
		self.params.window.deiconify()

		#while not self.params.window.state() == "withdrawn":
		#	sleep(0.001)

		#self.messageChecker.paused = False

	def checkMyEmail(self):
		self.receiveText.insert(END, "Checking...")
			# call receive in encodeDecode.py
			# if message found, set message (output of encodeDecode.py)

class MessageThread(Thread):
	def __init__(self, threadID, name, caller):
		'''creates a MessageThread object with attributes threadID, name, and running state'''
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.caller = caller

		self.paused = False
		self.killed = False

	def run(self):
		'''animates points from the two data queues'''
		while self.killed == False:
			if self.paused == False:
				a = 0
				#self.caller.checkMyEmail()
			else:
				#self.caller.receiveText.insert(END, "Paused")
				a = 1
			sleep(0.001)

class AlignWindow(Tk):
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")
		self.populateAlignWindow()

		# target GPS box, "virtual oscilloscope"
	def populateAlignWindow(self):
		self.addGPSEntry()
		self.addVirtualOscope()
		self.addControlButtons()

	def addGPSEntry(self):
		GPSEntryFrame = Frame(self.window)
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
		oscopeFrame = Frame(self.window)
		oscopeFrame.grid(row=1, column = 0)
		oscopeFrame.config(bg = "white")

		oscopeLabel = Label(oscopeFrame, text = "Photodiode Output", font = ("Sans Serif", 12, "bold"), bg = "white")
		oscopeLabel.pack(pady = 10)
 
	def addControlButtons(self):
		controlButtonsFrame = Frame(self.window)
		controlButtonsFrame.grid(row = 2, column = 0)
		controlButtonsFrame.config(bg = "white")

		startButton = Button(controlButtonsFrame, text = "Start", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "DarkGreen", activebackground = "green")
		bigRedButton = Button(controlButtonsFrame, text = "Stop", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "red", activebackground = "orange red")
		closeButton = Button(controlButtonsFrame, text = "Close", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan", command=self.close)
		

		startButton.grid(row = 0, column = 0, pady = "0 10")
		bigRedButton.grid(row = 0, column = 1, padx = 10, pady = "0 10")
		closeButton.grid(row = 0, column = 2, pady = "0 10")

	def setGPS(self):
		# set target GPS locally
		return 0

	def start(self):
		# send target GPS and AlignWindow object to align.py to start alignment procedure
		return 0

	def plot(self, diodeData):
		# update oscope readout
		return 0

	def stop(self):
		# stop thread in which start() in align.py is running
		return 0

	def close(self):
		self.window.withdraw()

	def setFinished(self):
		# boolean: alignment complete
		return 0

class ParamsWindow():
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")
		self.populateParamsWindow()
		# fields: PPM-level, pulse length, sample rate, threshold

	def populateParamsWindow(self):
		self.addParamsFields()
		self.addParamsButtons()

	def addParamsFields(self):
		paramsFieldsFrame = Frame(self.window)
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
		paramsButtonsFrame = Frame(self.window)
		paramsButtonsFrame.grid(row = 1, column = 0)
		paramsButtonsFrame.config(bg = "white")

		enterButton = Button(paramsButtonsFrame, text = "Enter", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan", command=self.updateParams)
		cancelButton = Button(paramsButtonsFrame, text = "Cancel", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "red", activebackground = "orange red", command=self.window.withdraw)

		enterButton.grid(row = 0, column = 0, padx = "0 10", pady = 10)
		cancelButton.grid(row = 0, column = 1, pady = 10)

	def updateParams(self):
		# read from fields and send to encodeDecode.py and hide ParamsWindow
		self.window.withdraw()
		return 0

if __name__ == "__main__":

	app = MainWindow(None)
	app.title("OpComms System IV Desktop Client")
	app.mainloop()