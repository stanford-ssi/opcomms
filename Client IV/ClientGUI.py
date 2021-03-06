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
import queue
import collections
import math
import ClassAlign

LONG_DELAY = 1000
DELAY = 1
DELAY_SEC = DELAY / 1000.0
READS = 50 #1000 // DELAY
MAX_READING = 1024.0
MAX_POS = 2**24

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
		self.after(LONG_DELAY, self.checkMyEmail)

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
		self.align.open()

	def openParams(self):
		messageChecker.pause()
		self.params.window.deiconify()

	def checkMyEmail(self):
		if not messageChecker.paused and not messageChecker.out.empty():
			status, received = messageChecker.out.get()
			if received: 
				self.receiveText.insert(END, "RX: " + received + "\n")
				self.receiveText.see(END)
		self.after(LONG_DELAY, self.checkMyEmail)

class AlignWindow:
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")
		self.window.protocol("WM_DELETE_WINDOW", self.close)
		self.homeGPS = [37.424157, -122.177866, 150] # latitude, longitude, altitude
		self.targetGPS = [37.424928, -122.176934, 100] # latitude, longitude, altitude
		self.populateAlignWindow()
		
		self.last_cmd = ""
		def raw(st, override=0, spd=0): 
			def pt(e): 
				if override or self.last_cmd != st:
					serialParser.raw(st)
					self.last_cmd = st
				if spd: self.speed = int(st)
			return pt
		
		for i in range(1, 10): self.window.bind("%d" % i, raw(str(i), spd=1))
		self.window.bind("<KeyRelease-Up>", raw("X"))
		self.window.bind("<KeyRelease-Down>", raw("X"))
		self.window.bind("<KeyRelease-Left>", raw("X"))
		self.window.bind("<KeyRelease-Right>", raw("X"))
		self.window.bind("<Up>", raw("U"))
		self.window.bind("<Down>", raw("D"))
		self.window.bind("<Left>", raw("L"))
		self.window.bind("<Right>", raw("R"))
		self.window.bind("`", raw("~", override=1))
		
		self.q_out = collections.deque()
		self.speed = 9; raw("9")
		#for i in range(self.oscope_width): self.q_out.append(0)
		self.oscopeThread = None
		self.alignment = None
		self.oldX, self.oldY = None, None
		self.posUpdating = True
	
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
		self.oscope_width = 600
		self.oscope_height = 300
		sensorControlsFrame = Frame(self.window)
		sensorControlsFrame.grid(row=1, column = 0)
		sensorControlsFrame.config(bg = "white")
		FONT = ("Sans Serif", 12, "bold")
		oscopeLabel = Label(sensorControlsFrame, text = "Photodiode Output", font = FONT, bg = "white")
		maxAvgFrame = Frame(sensorControlsFrame)
		kwargs={"font":FONT, "bg":"white", "width":10}
		self.oscopeMax = Label(maxAvgFrame, **kwargs)
		self.oscopeAvg = Label(maxAvgFrame, **kwargs)
		self.oscopeMax.grid(row=0, column=0)
		self.oscopeAvg.grid(row=0, column=1)
		#oscopeLabel.pack(pady = 10)
		self.oscope = Canvas(sensorControlsFrame, width = self.oscope_width, 
							height = self.oscope_height, bg = "black")
		self.angleDisplay = Canvas(sensorControlsFrame, width = 200, height = 300, bg = "white")
		self.oscopeSlider = Scale(sensorControlsFrame, from_=1.5, to=0,
								resolution=0.01, showvalue=False, length=self.oscope_height)
		self.oscopeSlider.set(0.5)
		oscopeLabel.grid(row = 0, column = 0)
		maxAvgFrame.grid(row=1, column=0)
		self.oscope.grid(row = 2, column = 0)
		self.oscopeSlider.grid(row=2, column=1)
		self.angleDisplay.grid(row = 2, column = 2)

		sensorControlsFrame.update_idletasks()

	def populateAngleDisplay(self, x, y):
		# 194 = Earth rotation speed; 46600 = 1 deg/s
		if x > MAX_POS/2: x -= MAX_POS
		if y > MAX_POS/2: y -= MAX_POS
		res = int(2 * ([0] + [x*194 for x in [2, 4, 8, 16, 32]] 
					+ [x*46600 for x in [.5, 1, 2, 4]])[self.speed])
		TOL = res/20
		if self.oldX is None or self.oldY is None or self.posUpdating > 5 \
				or (abs(x - self.oldX) < TOL and abs(y - self.oldY) < TOL):
			self.oldX, self.oldY = x, y
			self.posUpdating = 0
		else: 
			self.posUpdating += 1
			return
		width = self.angleDisplay.winfo_width()
		height = self.angleDisplay.winfo_height()
		diameter = 100
		pad = 30
		self.angleDisplay.delete(ALL)
		self.angleDisplay.create_line(width/2-pad, pad, width/2-pad, height-pad)
		self.angleDisplay.create_line(width-pad, pad, width-pad, height-pad)
		def create_triangle(x, y, display):
			display.create_polygon(x, y, x+pad/2, y-pad/4, x+pad/2, y+pad/4)
		create_triangle(width/2-pad, height/2, self.angleDisplay)
		create_triangle(width-pad, height/2, self.angleDisplay)
		scale = self.tickDistance(2*res)
		def drawLabels(xpos, x0):
			start = (x0 + res) // scale * scale
			for xi in range(start, x0 - res, -scale):
				xp = (x0 + res - xi) / (2*res) * height
				if xp > pad:
					self.angleDisplay.create_line(xpos-5, xp, xpos, xp)
					self.angleDisplay.create_text(xpos-pad, xp, text=str(xi))
		drawLabels(width/2-pad, x)
		drawLabels(width-pad, y)
		self.angleDisplay.create_text(width/2-2*pad, pad/2, text=str(x), fill='red')
		self.angleDisplay.create_text(width-2*pad, pad/2, text=str(y), fill='red')
		
	def addControlButtons(self):
		controlButtonsFrame = Frame(self.window)
		controlButtonsFrame.grid(row = 2, column = 0)
		controlButtonsFrame.config(bg = "white")

		startButton = Button(controlButtonsFrame, text = "Start", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "DarkGreen", activebackground = "green", command=self.start)
		bigRedButton = Button(controlButtonsFrame, text = "Stop", font = ("Sans Serif", 8, "bold"), fg = "white", bg = "red", activebackground = "orange red", command=self.stop)
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
	
	def tickDistance(self, height):
		height /= 2.5
		base = 10**int(math.log10(height))
		return int([-1, 1, 1, 2, 2, 2, 5, 5, 5, 5, 5][int(height/base)] * base)

	def plot(self):
		transform = lambda x: self.oscope_height - x*zoom
		self.oscope.delete(ALL)
		mult = 10 ** self.oscopeSlider.get()
		zoom = self.oscope_height * mult / MAX_READING
		units_top = MAX_READING / mult
		# round units_top to some nice round number
		scale = self.tickDistance(units_top)
		for i in range(0, int(units_top), scale):
			val = transform(i)
			self.oscope.create_line(0, val, self.oscope_width, val, fill="gray")
			self.oscope.create_text(20, val-10, text=str(i), fill="gray")
		def plotSeq(vals, color, tr):
			if not vals: return
			last = tr(vals[0])
			for i in range(len(vals)):
				val = tr(vals[i])
				self.oscope.create_line(i, last, i+1, val, fill=color)
				last = val
		
		reads = list(x[2] for x in self.q_out)
		if False and reads:
			reads_proc = np.array(reads) - np.mean(reads)
			fft = np.abs(np.fft.fft(reads_proc))
			fft = np.repeat(fft[:len(fft)/2], 2)
			mf, df = min(fft), max(fft) - min(fft)
			if df:
				fft = self.oscope_height * (1 - (fft - mf)/df)
				plotSeq(fft, "gray", lambda x: x)
		plotSeq(reads, "yellow", transform)
		reads = reads[-READS:]
		avg = sum(reads) / len(reads) if reads else 0
		avgv = transform(avg)
		self.oscope.create_line(0, avgv, self.oscope_width, avgv, 
							fill="red", dash=1)
		self.oscopeMax.config(text="MAX: %d" % max(reads) if reads else 0)
		self.oscopeAvg.config(text="AVG: %.1f" % avg)
		if self.q_out: 
			x, y, _ = self.q_out[-1]
			self.populateAngleDisplay(x, y)

	def start(self):
		self.alignment = AlignThread(3, "Align_Thread", self)
		self.alignment.start()
		self.oscope_stop()
	
	def stop(self):
		if self.alignment:
			self.alignment.kill()
			while self.alignment.is_alive(): pass
			print("Align killed")
			serialParser.raw("X")
			self.alignment = None
		self.oscope_start()
	
	def oscope_start(self):
		if self.oscopeThread:
			print("OScope already alive")
			return
		self.window.after(LONG_DELAY, self.checkOScope)
		self.oscopeThread = OScopeThread("OScopeThread", self)
		self.oscopeThread.start()
	
	def oscope_stop(self): 
		self.oscopeThread.killed = True
		self.oscopeThread = None
	
	def open(self):
		self.window.deiconify()
		self.oscope_start();

	def close(self):
		self.populateGPSFieldsFromStored()
		self.window.withdraw()
		messageChecker.resume()
		self.oscope_stop()
	
	def oscopeUpdate(self, x, y, val):
		qrem = self.oscopeThread.out.qsize()
		if qrem > 200: print("Falling behind by", qrem)
		self.q_out.append((x, y, val*1.2))
		if len(self.q_out) > self.oscope_width: self.q_out.popleft()
	
	def checkOScope(self):
		if self.oscopeThread:
			while not self.oscopeThread.out.empty():
				self.oscopeUpdate(*self.oscopeThread.out.get())
			self.plot()
			self.window.after(25, self.checkOScope)
	
class ParamsWindow:
	def __init__(self, parent):
		self.parent = parent
		self.window = Toplevel()
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.config(bg = "white")
		self.window.protocol("WM_DELETE_WINDOW", self.close)
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
	
class OScopeThread(Thread):
	def __init__(self, name, parent):
		Thread.__init__(self)
		self.name = name
		self.parent = parent
		self.out = queue.Queue()
		self.killed = False
		
	def run(self):
		print("OScope Run")
		while not self.killed: 
			self.out.put(serialParser.getPos())
			sleep(DELAY_SEC)
		print("OScope Killed")

class MessageThread(Thread):
	def __init__(self, threadID, name, parent):
		"""creates a MessageThread object with attributes threadID, name, and running state"""
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.parent = parent
		self.out = queue.Queue()

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
				msg = encodeDecode.receive()
				if msg[0] != encodeDecode.RCV_NO_MSG:
					self.out.put(msg)
			sleep(DELAY_SEC)

class AlignThread(Thread):  # How do I kill this in the middle of running functions?!  ...talk to Jake about making objects?
	def __init__(self, threadID, name, parent):
		"""creates an AlignThread object with attributes threadID, name, and running state"""
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.parent = parent
		self.align = ClassAlign.Align()

	def run(self): self.align.autoAlign()
	def kill(self): self.align.killed = True

if __name__ == "__main__":
	app = MainThread(2, "Main_Thread")
	messageChecker = MessageThread(1, "Message_Thread", app)
	messageChecker.start()
	app.start()
	app.window.openAlign()
	app.window.mainloop() # I'm not clear on why this needs to be done outside the thread's run method, but it seem like it does 

	messageChecker.killed = True

