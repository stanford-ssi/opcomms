from tkinter import *
from threading import *
from time import *

# import align

class MainWindow(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
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
		messageChecker.paused = True
		# calls send(whatever's in transmit box) method in encodeDecode.py
		messageChecker.paused = False

		return 0

	def openAlign(self):
		messageChecker.paused = True
		self.align.window.deiconify()

	def openParams(self):
		messageChecker.paused = True
		self.params.window.deiconify()

	def checkMyEmail(self):
		self.receiveText.delete(1.0, END)
		self.receiveText.insert(END, "Checking...")
			# call receive in encodeDecode.py
			# if message found, set message (output of encodeDecode.py)

class AlignWindow(Tk):
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")

		self.homeGPS = [37.424157, -122.177866, 150] # latitude, longitude, altitude
		self.targetGPS = [37.424928, -122.176934, 100] # latitude, longitude, altitude
		self.populateAlignWindow()

	def populateAlignWindow(self):
		self.addGPSEntry()
		self.addSensorControls()
		self.addControlButtons()

	def addGPSEntry(self):
		GPSEntryFrame = Frame(self.window)
		GPSEntryFrame.grid(row = 0, column = 0)
		GPSEntryFrame.config(bg = "white")

		GPSLabel = Label(GPSEntryFrame, text="Input GPS coordinates in decimal degrees", font=("Sans Serif", 12, "bold"), bg = "white")
		homeLabel = Label(GPSEntryFrame, text="HOME:", font=("Sans Serif", 12, "bold"), bg = "white")
		targetLabel = Label(GPSEntryFrame, text="TARGET:", font=("Sans Serif", 12, "bold"), bg = "white")

		self.homeLatField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		self.homeLongField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		self.homeAltField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		self.targetLatField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		self.targetLongField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		self.targetAltField = Entry(GPSEntryFrame, highlightthickness = 2, highlightcolor = "purple4", highlightbackground = "light slate gray")
		latitudeLabel = Label(GPSEntryFrame, text="Latitude", font=("Sans Serif", 10, "bold"), bg = "white")
		longitudeLabel = Label(GPSEntryFrame, text="Longitude", font=("Sans Serif", 10, "bold"), bg = "white")
		altitudeLabel = Label(GPSEntryFrame, text = "Altitude", font=("Sans Serif", 10, "bold"), bg = "white")
		GPSButton = Button(GPSEntryFrame, text = "Enter Coordinates", font = ("Sans Serif", 10, "bold"), fg = "white", bg = "purple4", activebackground = "purple", command=self.setGPS)

		GPSLabel.grid(row = 0, column = 0, columnspan = 4, pady  = "10 0")
		homeLabel.grid(row = 1, column = 0, pady =  "10 0")
		self.homeLatField.grid(row = 1, column = 1, padx = "10 5", pady =  "10 0")
		self.homeLongField.grid(row = 1, column = 2, padx = 5, pady = "10 0")
		self.homeAltField.grid(row = 1, column = 3, padx = 5, pady = "10 0")
		targetLabel.grid(row = 2, column = 0, pady =  "10 0")
		self.targetLatField.grid(row = 2, column = 1, padx = "10 5", pady =  "10 0")
		self.targetLongField.grid(row = 2, column = 2, padx = 5, pady = "10 0")
		self.targetAltField.grid(row = 2, column = 3, padx = 5, pady = "10 0")
		GPSButton.grid(row = 1, column = 4, rowspan=2, padx = "5 10", pady = "10 0")
		latitudeLabel.grid(row = 3, column = 1)
		longitudeLabel.grid(row = 3, column = 2)
		altitudeLabel.grid(row = 3, column = 3)

		self.populateGPSFieldsFromStored()

	def addSensorControls(self):
		sensorControlsFrame = Frame(self.window)
		sensorControlsFrame.grid(row=1, column = 0)
		sensorControlsFrame.config(bg = "white")

		oscopeLabel = Label(sensorControlsFrame, text = "Photodiode Output", font = ("Sans Serif", 12, "bold"), bg = "white")
		#oscopeLabel.pack(pady = 10)
		oscope = Canvas(sensorControlsFrame, width = 400, height = 300, bg = "black")
		controlArrows = Canvas(sensorControlsFrame, width = 100, height = 100, bg = "white")
		angleDisplay = Canvas(sensorControlsFrame, width = 200, height = 300, bg = "white")
	

		oscopeLabel.grid(row = 1, column = 0)
		oscope.grid(row = 2, column = 0)
		controlArrows.grid(row = 2, column = 1, padx = 10)
		angleDisplay.grid(row = 2, column = 2)

		sensorControlsFrame.update_idletasks()

		self.addControlArrows(controlArrows)
		self.populateAngleDisplay(angleDisplay)

	def addControlArrows(self, controlArrows):
		width = controlArrows.winfo_width()
		height = controlArrows.winfo_height()
		padding = 5
		upArrow = controlArrows.create_polygon(width/2, 0, width/3 + padding, height/3 - padding, 2*width/3 - padding, height/3 - padding)
		leftArrow = controlArrows.create_polygon(0, height/2, width/3 - padding, 2*height/3 - padding, width/3 - padding, height/3 + padding)
		downArrow = controlArrows.create_polygon(width/2, height, 2*width/3 - padding, 2*height/3 + padding, width/3 + padding, 2*height/3 + padding)
		rightArrow = controlArrows.create_polygon(width, height/2, 2*width/3 + padding, height/3 + padding, 2*width/3 + padding, 2*height/3 - padding)

		# upArrow.bind = ("<ButtonPress-1>", self.up_press)
		# upArrow.bind = ("<ButtonPress-1", self.up_release)
		# leftArrow.bind = ("<ButtonPress-1>", self.left_press)
		# leftArrow.bind = ("<ButtonPress-1", self.left_release)
		# downArrow.bind = ("<ButtonPress-1>", self.down_press)
		# downArrow.bind = ("<ButtonPress-1", self.down_release)
		# rightArrow.bind = ("<ButtonPress-1>", self.right_press)
		# rightArrow.bind = ("<ButtonPress-1", self.right_release)

	def up_press(self, event):
		self.configure(relief = "sunken")

	def up_release(self, event):
		self.configure(relief = "raised")

	def left_press(self, event):
		self.configure(relief = "sunken")

	def left_release(self, event):
		self.configure(relief = "raised")

	def down_press(self, event):
		self.configure(relief = "sunken")

	def down_release(self, event):
		self.configure(relief = "raised")

	def right_press(self, event):
		self.configure(relief = "sunken")

	def right_release(self, event):
		self.configure(relief = "raised")

	def populateAngleDisplay(self, angleDisplay):
		width = angleDisplay.winfo_width()
		print(width)
		height = angleDisplay.winfo_height()
		print(height)
		diameter = 100
		heightPadding = 50
		angleDisplay.create_oval([(width-diameter)/2, heightPadding, (width-diameter)/2+diameter, heightPadding+diameter])

	def populateAngleDisplay(self, angleDisplay):
		width = angleDisplay.winfo_width()
		height = angleDisplay.winfo_height()
		diameter = 100
		heightPadding = 10
		angleDisplay.create_oval([(width-diameter)/2, heightPadding, (width-diameter)/2+diameter, heightPadding+diameter], outline = "#9e9e9e")
		angleDisplay.create_arc([(width-diameter)/2, height-(heightPadding+diameter), (width-diameter)/2+diameter, height-heightPadding], extent = 180, outline = "#9e9e9e")
	
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

	def populateGPSFieldsFromStored(self):
		self.homeLatField.delete(0, END)
		self.homeLongField.delete(0, END)
		self.homeAltField.delete(0, END)
		self.targetLatField.delete(0, END)
		self.targetLongField.delete(0, END)
		self.targetAltField.delete(0, END)

		self.homeLatField.insert(0, self.homeGPS[0])
		self.homeLongField.insert(0, self.homeGPS[1])
		self.homeAltField.insert(0, self.homeGPS[2])
		self.targetLatField.insert(0, self.targetGPS[0])
		self.targetLongField.insert(0, self.targetGPS[1])
		self.targetAltField.insert(0, self.targetGPS[2])

	def setGPS(self):
		self.homeGPS[0] = self.homeLatField.get()
		self.homeGPS[1] = self.homeLongField.get()
		self.homeGPS[2] = self.homeAltField.get()
		self.targetGPS[0] = self.targetLatField.get()
		self.targetGPS[1] = self.targetLongField.get()
		self.targetGPS[2] = self.targetAltField.get()

	def start(self):
		#self.alignment = AlignThread(3, "Align_Thread", self)
		#self.alignment.start()

		return 0

	def plot(self, diodeData):
		# update oscope readout
		return 0

	def stop(self):
		#if self.alignment.isAlive():
		#	alignment.killed = True
		return 0

	def close(self):
		self.populateGPSFieldsFromStored()
		self.window.withdraw()
		messageChecker.paused = False

	def setFinished(self):
		# boolean: alignment complete
		return 0

class ParamsWindow():
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")
		
		self.values = [4, 1000, 1000, 5] # fields: PPM-level, pulse length, sample rate, threshold
		self.populateParamsWindow()

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

		self.ppmLevelField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")
		self.pulseLengthField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")
		self.sampleRateField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")
		self.thresholdField = Entry(paramsFieldsFrame, highlightthickness = 2, highlightcolor = "cyan4", highlightbackground = "light slate gray")

		self.populateFieldsFromStored()

		parametersTitle.grid(row = 0, column = 0, columnspan = 2)
		ppmLevelLabel.grid(row = 1, column = 0, padx =  10, pady = "10 5")
		self.ppmLevelField.grid(row = 1, column = 1, padx = "0 10", pady = "10 5")
		pulseLengthLabel.grid(row = 2, column = 0, padx = 10, pady = 5)
		self.pulseLengthField.grid(row = 2, column = 1, padx = "0 10", pady =  5)
		sampleRateLabel.grid(row = 3, column = 0, padx = 10, pady = 5)
		self.sampleRateField.grid(row = 3, column = 1, padx = "0 10", pady = 5)
		thresholdLabel.grid(row = 4, column = 0, padx = 10, pady = "5 10")
		self.thresholdField.grid(row = 4, column = 1, padx = "0 10", pady = "5 10")

	def addParamsButtons(self):
		paramsButtonsFrame = Frame(self.window)
		paramsButtonsFrame.grid(row = 1, column = 0)
		paramsButtonsFrame.config(bg = "white")

		enterButton = Button(paramsButtonsFrame, text = "Enter", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan", command=self.updateParams)
		cancelButton = Button(paramsButtonsFrame, text = "Cancel", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "red", activebackground = "orange red", command=self.close)

		enterButton.grid(row = 0, column = 0, padx = "0 10", pady = 10)
		cancelButton.grid(row = 0, column = 1, pady = 10)

	def populateFieldsFromStored(self):
		self.ppmLevelField.delete(0, END)
		self.ppmLevelField.insert(0, self.values[0])
		self.pulseLengthField.delete(0, END)
		self.pulseLengthField.insert(0, self.values[1])
		self.sampleRateField.delete(0, END)
		self.sampleRateField.insert(0, self.values[2])
		self.thresholdField.delete(0, END)
		self.thresholdField.insert(0, self.values[3])

	def updateParams(self):
		self.values[0] = self.ppmLevelField.get()
		self.values[1] = self.pulseLengthField.get()
		self.values[2] = self.sampleRateField.get()
		self.values[3] = self.thresholdField.get()

		self.window.withdraw()
		messageChecker.paused = False

	def close(self):
		self.populateFieldsFromStored()
		self.window.withdraw()
		messageChecker.paused = False

class MainThread(Thread):
	def __init__(self, threadID, name):
		'''creates a MainThread object with attributes threadID, name, and running state'''
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.window = MainWindow(None)
		self.window.title("OpComms System IV Desktop Client")

	def run(self):
		return 0

class MessageThread(Thread):
	def __init__(self, threadID, name, parent):
		'''creates a MessageThread object with attributes threadID, name, and running state'''
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.parent = parent

		self.paused = True
		self.killed = False

	def run(self):
		while self.killed == False:
			if self.paused == False:
				self.parent.window.checkMyEmail()
			sleep(0.1)

class AlignThread(Thread):  # How do I kill this in the middle of running functions?!  ...talk to Jake about making objects?
	def __init__(self, threadID, name, parent):
		'''creates an AlignThread object with attributes threadID, name, and running state'''
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.parent = parent

		self.killed = False

	def run(self):
		align.roughAlign(HOME, targetGPS)
		align.lockOn(threshold, initialSpread)

if __name__ == "__main__":
	app = MainThread(2, "Main_Thread")
	messageChecker = MessageThread(1, "Message_Thread", app)

	messageChecker.start()
	app.start()
	app.window.openAlign()
	app.window.mainloop() # I'm not clear on why this needs to be done outside the thread's run method, but it seem like it does 

	messageChecker.killed = True

