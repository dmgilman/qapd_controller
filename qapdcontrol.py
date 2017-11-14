from Tkinter import *
import time
import piplates.DAQCplate as DAQC
import tkFont
import string
import numpy as np

data = np.empty(shape=[0,3])

fb_initialBias = -275
fb_slope = -9.57
fb_percent = .25
fb_nominalTemp = 3.0752
fb_bias = fb_initialBias + fb_slope*fb_percent*(DAQC.getADC(0,0)-fb_nominalTemp)

class titleBLOCK:
	def __init__(self, master, r, c):
		self.master=master
		self.tit = Frame(self.master,padx=4,pady=4,bd=2,bg='white',relief='sunken')
		self.tit.grid(row=r,column=c,columnspan=2,sticky=N+S+E+W)
		
		##Fonts
		self.title = tkFont.Font(family='Helvetica', size=30, weight='bold')
		self.heading = tkFont.Font(family='Helvetica', size=18, weight='bold')
		
		##Title
		self.labelt = Label(self.tit, text="QAPD Controller", bg='white', fg='green',padx=4,pady=4,font=self.title, anchor='center')
		self.labelt.grid(row=0, column=0, columnspan=3, sticky=W+E)
		
		##Close button
		self.close_button = Button(self.tit, text="X", command=root.quit).grid(row=1,column=2,sticky=E)
		
		def shutdown(self, event):
			print "clicked at", event.x, event.y


class lightBLOCK:
	def __init__(self, master, r, c):
		self.master=master
		self.lm=Frame(self.master,padx=4,pady=4,bd=2,relief='sunken')
		self.lm.grid(row=r,column=c,sticky=N+S+W+E)
		
		##Fonts
		self.title = tkFont.Font(family='Helvetica', size=24, weight='bold')
                self.heading = tkFont.Font(family='Helvetica', size=16, weight='bold')
		self.normal = tkFont.Font(family='Helvetica', size=14)
		
		##Title
		self.labelt = Label(self.lm, text="LED", padx=4,pady=4, font=self.title)
		self.labelt.grid(row=0,column=0, columnspan=2, sticky=W+E)

		##LED Voltage slider
		self.heading1 = Label(self.lm, text="Voltage (V)",padx=4,pady=4,font=self.heading)
		self.heading1.grid(row=1,column=0)
		self.voltage = DoubleVar()
		self.voltage.set(0)
		self.voltageSet = Scale(self.lm, variable=self.voltage, from_=0, to=4, resolution=0.05, width=30, length=120)
		self.voltageSet.bind("<ButtonRelease-1>", self.vdelta)
		self.voltageSet.grid(row=2,column=0,rowspan=2)

		##LED switch
		self.heading2 = Label(self.lm, text="ON/OFF",padx=4,pady=4, font=self.heading)
		self.state = StringVar()
		self.state.set("OFF")
		self.labelc = Label(self.lm, textvariable=self.state, padx=4,pady=4,font=self.normal, fg='green', anchor=S)
		self.switch = Checkbutton(self.lm, variable=self.state, onvalue= "ON", offvalue = "OFF", anchor=N)
		self.switch.bind("<ButtonRelease-1>", self.vdelta)
		self.heading2.grid(row=1,column=1)
		self.labelc.grid(row=2,column=1, sticky=N+S+E+W)
		self.switch.grid(row=3,column=1, sticky=N+S+E+W)

	##update output LED voltage
	def vdelta(self,val):
		if (self.state.get()=="ON"):
			DAQC.setDAC(0,0,self.voltage.get())
		else: 
			DAQC.setDAC(0,0,0)
		print "LED V:", DAQC.getDAC(0,0)

class biasBLOCK:
	def __init__(self,master,r,c):
                self.master=master
                self.bm=Frame(self.master,padx=4,pady=4,bd=2,relief='sunken')
                self.bm.grid(row=r,column=c,sticky=N+S+W+E)

                ##Fonts
                self.title = tkFont.Font(family='Helvetica', size=24, weight='bold')
                self.heading = tkFont.Font(family='Helvetica', size=16, weight='bold')
                self.normal = tkFont.Font(family='Helvetica', size=14)

                ##Title
                self.labelt = Label(self.bm, text="Bias (V)", padx=4,pady=4, font=self.title)
                self.labelt.grid(row=0,column=0, columnspan=2, sticky=W+E)

                ##LED Voltage slider
		##output voltage (o), desired bias voltage (b)
		##b=60o-300 -> o=b/60+5
                self.heading1 = Label(self.bm, text="Bias Voltage",padx=4,pady=4,font=self.heading)
                self.heading1.grid(row=1,column=0)
		self.instructions = Label(self.bm, text="Input range from -300 to -50", padx=4, pady=4).grid(row=2, column=0)
                self.voltage = DoubleVar()
                self.voltage.set(-275)
		self.voltageSet = Entry(self.bm, textvariable=self.voltage, width=5)
                #self.voltageSet = Scale(self.bm,variable=self.voltage, from_=-300, to=-60, resolution=1, width=30, length=240)
                #self.voltageSet.bind("<ButtonRelease-1>", self.vdelta)
                self.voltageSet.grid(row=3,column=0,rowspan=1)

                ##switch
                self.heading2 = Label(self.bm, text="ON/OFF",padx=4,pady=4, font=self.heading)
                self.state = StringVar()
                self.state.set("OFF")
                self.labelc = Label(self.bm, textvariable=self.state, padx=4,pady=4,font=self.normal, fg='green', anchor=S)
                self.switch = Checkbutton(self.bm, variable=self.state, onvalue= "ON", offvalue = "OFF", anchor=N)
                #self.switch.bind("<ButtonRelease-1>", self.vdelta)
                self.heading2.grid(row=1,column=1)
                self.labelc.grid(row=2,column=1,sticky=N+E+W+S)
                self.switch.grid(row=3,column=1,sticky=N+E+W+S)

                ##FB Switch
                self.fb_button = Button(self.bm, text = "Feedback Mode", command=self.fbMode).grid(row=5, column=0)
                ##update voltage button
		self.update_button = Button(self.bm, text = "Update", command=self.vdelta).grid(row=4,column=0)

        ##update output bias voltage
        def vdelta(self):
                if (self.state.get()=="ON"):
                        x = self.voltage.get()/60.84+4.9
			if (x<0): x = 0
			if (x>4.095): x = 4.095
			DAQC.setDAC(0,1,x)
                else:
                        DAQC.setDAC(0,1,0)
                print "bias V:", DAQC.getDAC(0,1)

        def fbMode(self):
                self.voltage.set(fb_bias)
                root.after(500, self.fbMode)

class voltageDisplay:
	def __init__(self,master,title,channel,r,c):
                self.master=master
		self.channel=channel
                self.tm=Frame(self.master,padx=4,pady=4,bd=2,relief='sunken')
                self.tm.grid(row=r,column=c,sticky=N+S+W+E)

                ##Fonts
                self.title = tkFont.Font(family='Helvetica', size=24, weight='bold')
                self.heading = tkFont.Font(family='Helvetica', size=16, weight='bold')
                self.normal = tkFont.Font(family='Helvetica', size=14)

                ##Title
                self.labelt = Label(self.tm, text=title, padx=4,pady=4, font=self.title)
                self.labelt.grid(row=0,column=0, columnspan=2, sticky=W+E)

		##display
		self.labelv1 = Label(self.tm, text="Voltage:",  font=self.heading, anchor=E)
		self.labelv1.grid(row=1,column=0, sticky=W+E)
		self.tvoltage = DoubleVar()
		self.tvoltage.set(DAQC.getADC(0,channel))
		self.labelv2 = Label(self.tm, textvariable=self.tvoltage, font=self.heading, fg='green', anchor=W)
		self.labelv2.grid(row=1,column=1, sticky=W+E)

		##update button, until better solution found
		self.buttonu = Button(self.tm, text="Update", command=self.update, padx=4, pady=4)
		self.buttonu.grid(row=2, column=0, columnspan=2, sticky=W+E)

	def update(self):
		self.tvoltage.set(DAQC.getADC(0,self.channel))
		root.after(500, self.update)

class tempDisplay:
	def __init__(self,master,channel,r,c):
		self.master=master
		self.channel=channel
		self.tm=Frame(self.master,padx=4,pady=4,bd=2,relief='sunken')
		self.tm.grid(row=r,column=c,sticky=N+S+W+E)

		##Font
                self.heading = tkFont.Font(family='Helvetica', size=18, weight='bold')

                ##Title
                self.labelt = Label(self.tm, text="Temperature (C):", padx=4,pady=4, font=self.heading)
                self.labelt.grid(row=0, sticky=W+E)

		##display
		self.temp = DoubleVar()
		self.temp.set(18.14*DAQC.getADC(0,channel)-20.32)
		self.tempLabel = Label(self.tm, textvariable=self.temp, font=self.heading, fg='green')
		self.tempLabel.grid(row=1, sticky=W+E)

		##update button, until better solution found
                self.buttonu = Button(self.tm, text="Update", command=self.update, padx=4, pady=4)
                self.buttonu.grid(row=2, sticky=W+E)

        def update(self):
                x = (18.14*DAQC.getADC(0,self.channel)-20.32)
		self.temp.set('%.3f'%x)
                root.after(500, self.update)

class dataLog:
	def __init__(self,master,channel1,channel2,r,c):
		self.master=master
		self.tempChannel = channel1
		self.sumChannel = channel2
		self.dm=Frame(self.master,padx=4,pady=4,bd=2,relief='sunken')
                self.dm.grid(row=r,column=c,sticky=N+S+W+E)
		
		##Logger Toggle button
		self.logstate = StringVar()
		self.logstate.set("Not Logging")
		self.loglabel = Label(self.dm, text="Log Data?", padx=4, pady=4).grid(row=0,column=0, sticky=E)
		self.logbox = Button(self.dm, textvariable=self.logstate, command=self.logToggle, fg='green', padx=4,pady=4)
		self.logbox.grid(row=0,column=1,sticky=W)

		##SaveButton and entry
		self.fname = StringVar()
		self.fname.set(".csv")
		self.fileNameEntry = Entry(self.dm, textvariable=self.fname, justify=RIGHT, width=20)
		self.fileNameEntry.grid(row=1,column=0,sticky=E)
		self.saveButton = Button(self.dm, text="Save", command=self.saveData, padx=4, pady=4)
		self.saveButton.grid(row=1,column=1,sticky=W)

		##clear data button
                self.clearButton = Button(self.dm, text="Clear Data", command=self.clearData, padx=4, pady=4)
                self.clearButton.grid(row=3,column=0,sticky=E)

		##Adjusts the subinterval length in logdata function. Probably want to deactivate this Entry box while logging data.
		self.subInterval = IntVar()
		self.subInterval.set(1000)
		self.intervalEntry = Entry(self.dm, textvariable=self.subInterval,  width=6)
		self.intervalEntry.grid(row=2,column=1,sticky=W)
		self.intLabel = Label(self.dm, text="Log subinterval (ms):", padx=4,pady=4).grid(row=2,column=0,sticky=E)
		
		
	#basically giving this button a similar functionality to a checkbox, but with an easily built in command when toggled			
	def logToggle(self):
		if (self.logstate.get() == "Not Logging"):
			self.logstate.set("Logging")
			self.logData()
		elif (self.logstate.get() == "Logging"):
			self.logstate.set("Not Logging")

	#records a SUM voltage reading 10x then taking the average of those before
	#adding that and the temperature voltage to the log then waiting the subinterval before repeating
	#maybe want to do the same for temperature as well to be consistent, though the temp doesn't vary near as much or as quickly
	def logData(self):
		global data
		if (self.logstate.get() == "Logging"):
			print "Logging..."
			sampleSet = np.zeros(shape=[10,1])
			for x in range(10):
				sampleSet[x] = DAQC.getADC(0,self.sumChannel)
			averageSum = np.mean(sampleSet)
			data = np.append(data, [[DAQC.getADC(0,self.tempChannel), averageSum, fb_bias]], axis=0)
		root.after(self.subInterval.get(), self.logData)

	def saveData(self):
		global data
		if (self.fname.get() == ".csv"):
			self.fname.set("log.csv")
		##probably want to add some additional error handling here, but should suffice for now
		print data
		print "saved to", self.fname.get()
		np.savetxt(self.fname.get(),data,delimiter=",",fmt="%.3e")

	def clearData(self):
		global data
		data = np.empty(shape=[0,3])
		print "data cleared"


	
root = Tk()
#root.config(bg="black")
#root.attributes("-fullscreen", True)
#swidth=root.winfo_screenwidth()
#sheight=root.winfo_screenheight()
container = Frame(root, bg='white')
container.pack()
#container.place(relx=0.5, rely=0.5, anchor=CENTER)

title = titleBLOCK(container,0,0)
led = lightBLOCK(container,1,0)
bias = biasBLOCK(container,1,1)
temp = voltageDisplay(container,"Temperature",0,2,0)
temp2 = tempDisplay(container,0,3,0)
sum = voltageDisplay(container,"QAPD Sum",1,2,1)
log = dataLog(container,0,1,3,1)

root.mainloop()

#make sure output voltage is off
DAQC.setDAC(0,0,0)
DAQC.setDAC(0,1,0)
