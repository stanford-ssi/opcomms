""" `
ClientGUI.py
Stanford Space Initative, Optical Communications Project
Authors: Elizabeth Hillstrom, Tara Iyer

ClientGUI is the user interface for OpComms System IV, providing access to alignment, transmit, and receive functionality
"""


from tkinter import *
from threading import *
from time import *

import encodeDecode
import serialParser

class MainWindow(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.protocol("WM_DELETE_WINDOW", self.quit)
		self.parent = parent
		self.resizable(width=FALSE, height=FALSE)
		self.config(bg = "white")
		self.transmitFrame()
		self.receiveFrame()
		self.optionsFrame()
		self.update_idletasks()
		#self.receiveText.insert(END, "Hello!")

		self.align = AlignWindow(self)
		self.align.window.title("Align Node")
		self.align.window.withdraw()

		self.params = ParamsWindow(self)
		self.params.window.title("Set PPM Parameters")
		self.params.window.withdraw()

	def transmitFrame(self):
		"""Create Transmit Canvas and populate with label, entry box, and button"""

		transmitFrame = Frame(self)
		transmitFrame.grid(column=0, columnspan=2, row=0, rowspan=3)
		transmitFrame.config(bg = "white")

		transmitLabel = Label(transmitFrame, text="Transmit", font=("Sans Serif", 20, "bold"), fg="#006400", bg = "white")
		transmitEntryLabel = Label(transmitFrame, text = "(Instructions for Transmit Input)", font = ("Times New Roman", 9), fg="black", bg = "white")
		self.transmitEntry = Entry(transmitFrame, width=30, fg="green", highlightthickness = 2, highlightcolor = "green", highlightbackground = "light slate gray")
		self.transmitEntry.bind("<Return>", lambda e: self.transmit())
		transmitButton = Button(transmitFrame, text="SEND", font=("Arial", 8, "bold"), fg="white", bg="green", activebackground = "DarkGreen", command=self.transmit)

		transmitLabel.pack(pady= '10 0')
		transmitEntryLabel.pack(padx = 10, pady = "35 10")
		self.transmitEntry.pack(padx = 10)
		transmitButton.pack(pady = 10)

	def receiveFrame(self):
		"""Create Receive Canvas and populate with label and entry box"""
		receiveFrame = Frame(self)
		receiveFrame.grid(column=2, columnspan=2, row=0, rowspan=6)
		receiveFrame.config(bg = "white")

		receiveLabel = Label(receiveFrame, text="Receive", font=("Sans Serif", 20, "bold"), fg="blue", bg = "white")
		self.receiveText = Text(receiveFrame, width=67, height = 10, fg = "blue", highlightthickness = 2, highlightcolor = "blue", highlightbackground = "light slate gray")

		receiveLabel.pack(pady="10 0")
		self.receiveText.pack(padx = 10, pady = 10)

	def optionsFrame(self):
		"""Create Options Canvas and populate with buttons"""
		optionsFrame = Frame(self)
		optionsFrame.grid(column=0, columnspan=2, row=5)
		optionsFrame.config(bg = "white")

		alignButton = Button(optionsFrame, text="Align", font=("Arial", 8, "bold"), fg = "white", bg = "purple4", activebackground = "purple", command = self.openAlign)
		paramsButton = Button(optionsFrame, text="Set Parameters", font = ("Arial", 8, "bold"), fg = "white", bg = "cyan4", activebackground = "cyan", command = self.openParams)

		alignButton.grid(column=0, row = 0, padx = 5, pady = "0 10")
		paramsButton.grid(column=1, row = 0, padx = 5, pady = "0 10")

	def transmit(self):
		messageChecker.pause()
		msg = self.transmitEntry.get()
		if not msg: return
		encodeDecode.send(msg)
		self.receiveText.insert(END, "TX: " + msg + "\n")
		self.transmitEntry.delete(0, END)
		messageChecker.resume()

	def openAlign(self):
		messageChecker.pause()
		self.align.window.deiconify()

	def openParams(self):
		messageChecker.pause()
		self.params.window.deiconify()

	def checkMyEmail(self):
		status, received = encodeDecode.receive()
		def insert_text():	
			if received: 
				self.receiveText.insert(END, "RX: " + received + "\n")
				self.receiveText.see(END)
		self.after(0, insert_text)

class AlignWindow(Tk):
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")

		self.homeGPS = [37.424157, -122.177866, 150] # latitude, longitude, altitude
		self.targetGPS = [37.424928, -122.176934, 100] # latitude, longitude, altitude
		self.populateAlignWindow()
		
		self.last_cmd = ""
		def raw(st, override=0): 
			def pt(e): 
				if override or self.last_cmd != st:
					serialParser.raw(st)
					print("Raw command:", st)
					self.last_cmd = st
			return pt
		
		for i in range(1, 10): self.window.bind("%d" % i, raw(str(i)))
		self.window.bind("<KeyRelease-Up>", raw("X"))
		self.window.bind("<KeyRelease-Down>", raw("X"))
		self.window.bind("<KeyRelease-Left>", raw("X"))
		self.window.bind("<KeyRelease-Right>", raw("X"))
		self.window.bind("<Up>", raw("U"))
		self.window.bind("<Down>", raw("D"))
		self.window.bind("<Left>", raw("L"))
		self.window.bind("<Right>", raw("R"))
		self.window.bind("`", raw("~", override=1))
		
		

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
		angleDisplay = Canvas(sensorControlsFrame, width = 200, height = 300, bg = "white")
	

		oscopeLabel.grid(row = 1, column = 0)
		oscope.grid(row = 2, column = 0)
		angleDisplay.grid(row = 2, column = 2)

		sensorControlsFrame.update_idletasks()
		self.populateAngleDisplay(angleDisplay)

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
		self.homeGPS[0] = float(self.homeLatField.get())
		self.homeGPS[1] = float(self.homeLongField.get())
		self.homeGPS[2] = float(self.homeAltField.get())
		self.targetGPS[0] = float(self.targetLatField.get())
		self.targetGPS[1] = float(self.targetLongField.get())
		self.targetGPS[2] = float(self.targetAltField.get())
		asc = align.getGPSAscension(self.homeGPS, self.targetGPS)
		azi = align.getGPSAzimuth(self.homeGPS, self.targetGPS)
		serialParser.moveTo(azi, asc)

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
		messageChecker.resume()

	def setFinished(self):
		# boolean: alignment complete
		return 0

class ParamsWindow():
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")
		
		self.values = [4, 100, 10, 5] # fields: PPM-level, pulse length, sample rate, threshold
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
		compressLabel = Label(paramsFieldsFrame, text = "Compress?", font = ("Sans Serif", 10, "bold"), bg = "white")
		checksumLabel = Label(paramsFieldsFrame, text = "Use checksum?", font = ("Sans Serif", 10, "bold"), bg = "white")

		self.compressVar = IntVar()
		self.checksumVar = IntVar()
		
		kwargs = { "highlightthickness" : 2, 
				"highlightcolor" : "cyan4", 
				"highlightbackground" : "light slate gray"}
		
		self.ppmLevelField = Entry(paramsFieldsFrame, **kwargs)
		self.pulseLengthField = Entry(paramsFieldsFrame, **kwargs)
		self.sampleRateField = Entry(paramsFieldsFrame, **kwargs)
		self.thresholdField = Entry(paramsFieldsFrame, **kwargs)
		self.compressBox = Checkbutton(paramsFieldsFrame, variable=self.compressVar, **kwargs)
		self.checksumBox = Checkbutton(paramsFieldsFrame, variable=self.checksumVar, **kwargs)
		
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
		
		compressLabel.grid(row = 5, column = 0, padx = 10, pady = "5 10")
		self.compressBox.grid(row = 5, column = 1, padx = "0 10", pady = "5 10")
		
		checksumLabel.grid(row = 6, column = 0, padx = 10, pady = "5 10")
		self.checksumBox.grid(row = 6, column = 1, padx = "0 10", pady = "5 10")

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
		encodeDecode.setOptions(compress=self.compressVar.get(),
							use_cksum=self.checksumVar.get())
		serialParser.raw("O %d %d %d" % tuple(int(i) for i in self.values[1:]))
		self.window.withdraw()
		messageChecker.resume()

	def close(self):
		self.populateFieldsFromStored()
		self.window.withdraw()
		messageChecker.resume()

class MainThread(Thread):
	def __init__(self, threadID, name):
		"""creates a MainThread object with attributes threadID, name, and running state"""
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.window = MainWindow(None)
		self.window.title("OpComms System IV Desktop Client")

	def run(self):
		return 0

class MessageThread(Thread):
	def __init__(self, threadID, name, parent):
		"""creates a MessageThread object with attributes threadID, name, and running state"""
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.parent = parent

		self.paused = True
		self.killed = False
		
	def pause(self): 
		print("Pausing Receive Mode")
		self.paused = True
	
	def resume(self): 
		print("Resuming Receive Mode")
		self.paused = False

	def run(self):
		while self.killed == False:
			if self.paused == False:
				self.parent.window.checkMyEmail()
			sleep(0.1)

class AlignThread(Thread):  # How do I kill this in the middle of running functions?!  ...talk to Jake about making objects?
	def __init__(self, threadID, name, parent):
		"""creates an AlignThread object with attributes threadID, name, and running state"""
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

