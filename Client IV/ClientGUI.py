from tkinter import *
from threading import *
from time import *

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

		# self.openAlign()

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
		'''animates points from the two data queues'''
		print("Starting MessageThread")
		while self.killed == False:
			if self.paused == False:
				self.parent.window.checkMyEmail()
			sleep(0.1)


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
		self.addSensorControls()
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
		cancelButton = Button(paramsButtonsFrame, text = "Cancel", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "red", activebackground = "orange red", command=self.close)

		enterButton.grid(row = 0, column = 0, padx = "0 10", pady = 10)
		cancelButton.grid(row = 0, column = 1, pady = 10)

	def updateParams(self):
		# read from fields and send to encodeDecode.py and hide ParamsWindow
		self.window.withdraw()
		messageChecker.paused = False

	def close(self):
		self.window.withdraw()
		messageChecker.paused = False

class MainThread(Thread):
	def __init__(self, threadID, name):
		'''creates a MessageThread object with attributes threadID, name, and running state'''
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.window = MainWindow(None)
		self.window.title("OpComms System IV Desktop Client")

	def run(self):
		print("Starting MainThread")

if __name__ == "__main__":
	app = MainThread(2, "Thread-2")
	messageChecker = MessageThread(1, "Thread-1", app)

	messageChecker.start()
	app.start()
	app.window.openAlign()
	app.window.mainloop() # I'm not clear on why this needs to be done outside the thread's run method, but it seem like it does 

	messageChecker.killed = True

