from tkinter import *

class MainWindow():
	def __init__(self, master=None):
		root = Tk()
		windowWidth = 800
		windowHeight = 600
		root.geometry('{}x{}'.format(windowWidth, windowHeight))
		root.resizable(width=TRUE, height=TRUE)
		root.update_idletasks()
		self.populateWindow(root)
		root.mainloop()
		# creates ClientGUI Window w/ TX box, RX box, buttons
		# put checkMyEmail() in its own thread
		# instantiate an AlignWindow
		# call alignButton() [purpose of this is to force checkMyEmail to block/unblock properly]
		# instantiate a ParamsWindow
		# hide ParamsWindow

	def populateWindow(self, root):
		# make Transmit and Receive labels
		transmitLabel = Label(root,text="Transmit",font=("Arial", 20),fg="green")
		transmitLabel.place(x=(root.winfo_width()*(1/4) - transmitLabel.winfo_width()*(1/2)), y=(root.winfo_height()*(1/8) - transmitLabel.winfo_height()*(1/2)))
		receiveLabel = Label(root,text="Receive",font=("Arial", 20),fg="blue")
		receiveLabel.place(x=(root.winfo_width()*(3/4) - receiveLabel.winfo_width()*(1/2)), y=(root.winfo_height()*(1/8) - receiveLabel.winfo_height()*(1/2)))

		# make Transmit text box and button
		transmitButton = Button(root,text="Enter Transmission")
		transmitButton.place(x=(root.winfo_width()*(1/4) - transmitButton.winfo_width()*(1/2)), y=(root.winfo_height()*(3/4) - transmitButton.winfo_height()*(1/2)))
		transmitButton.bind('<Transmit_Button>',self.transmit())

		# make Receive text box

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


