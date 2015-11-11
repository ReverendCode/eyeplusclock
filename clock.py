__author__ = 'ReverendCode' # I suppose this is because I have this project checked into bitbucket, where this is my username?
#comments in python use the pound thingy

from tkinter import *
from sound import Sound
import os

class SetUp: #Prepare the canvas
    def __init__(self, parent):
        self.myParent = parent
        # Set up key bindings
        self.myParent.bind("<j>", self.leftPress)
        self.myParent.bind("<k>", self.rightPress)
        self.myParent.bind("<space>", self.selectPress)

        self.rootContainer = Frame(parent, width=50, height = 20)
        self.rootContainer.pack()
        # Create and order the frames needed.
        self.displayFrame = Frame(self.rootContainer)
        self.displayFrame.pack(side=TOP)
        # In the interest of clarity, maybe set things up in order.

        self.timeDisplay = Label(self.displayFrame, text = "Current Time!")
        self.timeDisplay.pack()
        self.menuFrame = Frame(self.rootContainer)
        self.menuFrame.pack(side=TOP)

        # Create the main menu strip

        self.menuLabel1 = self.makeStaticLabel(self.menuFrame, "Main Menu")
        self.menuLabel1.pack(side=LEFT)
        self.menuLabelSpace = Label(self.menuFrame, width=2)
        self.menuLabelSpace.pack(side=LEFT)
        self.menuLabel2 = self.makeStaticLabel(self.menuFrame, "Set Day")
        self.menuLabel2.pack(side=LEFT)
        self.menuLabel2.configure(state='active') # Start with the first option selected by default

        self.menuLabel3 = self.makeStaticLabel(self.menuFrame, "Set Hour")
        self.menuLabel3.pack(side=LEFT)
        self.menuLabel4 = self.makeStaticLabel(self.menuFrame, "Set Minute")
        self.menuLabel4.pack(side=LEFT)

        # Set up some arrays
        self.menu = [self.menuLabel2, self.menuLabel3, self.menuLabel4]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


        # Build sound arrays, Programmatically
        MENUS = "./sounds/menu_navigation/"
        self.menuSounds = [
            Sound(MENUS + "Set_day_of_week_f.wav"),
            Sound(MENUS + "Set_hour_f.wav"),
            Sound(MENUS + "Set_minutes_f.wav")
        ]


        # Create variables to plug into the selection labels
        # heading, left left, left, right, right right
        self.headingVar = StringVar()
        self.llVar = StringVar()
        self.lVar = StringVar()
        self.rVar = StringVar()
        self.rrVar = StringVar()
        self.listofVars = [self.llVar, self.lVar, self.rVar, self.rrVar]

        self.selectionFrame = Frame(self.rootContainer)
        self.selectionFrame.pack(side=TOP)
        # Generate blank labels to be filled
        self.label1 = self.makeVarLabel(self.selectionFrame, self.headingVar)
        self.label1.pack(side=LEFT)
        self.labelSpace = Label(self.selectionFrame, width=2)
        self.labelSpace.pack(side=LEFT)
        self.labelLL = self.makeVarLabel(self.selectionFrame, self.llVar)
        self.labelLL.pack(side=LEFT)
        self.labelL = self.makeVarLabel(self.selectionFrame, self.lVar)
        self.labelL.pack(side=LEFT)
        self.labelR = self.makeVarLabel(self.selectionFrame,self.rVar)
        self.labelR.pack(side=LEFT)
        self.labelRR = self.makeVarLabel(self.selectionFrame, self.rrVar)
        self.labelRR.pack(side=LEFT)
        # Disable selection frame
        for child in self.selectionFrame.winfo_children():
            child.configure(state='disable')

        self.varLabels = [self.labelLL, self.labelL, self.labelR, self.labelRR]
        #Set up variables for menus

        self.selectionActive = False # Toggle between menu bar and selection bar
        self.anteMeridian = True # AM / PM

        # have I mentioned how much I like indices?
        self.menuIndex = 0 # 0-2
        self.dayIndex = 0 # 0-6
        self.hourIndex = 0 # 0-23
        self.minuteIndex = 0 # 0-59
        self.selectPosition = 0 # 0-3
        self.updateSelectionMenu()


    def selectMove(self, newPosition): # New position should be one of -1, 0, 1
        if self.menuIndex == 0: # Load the "Days" menu options
            self.dayIndex += newPosition
            # self.displayDays()
        if self.menuIndex == 1: # Load the hours Menu options
            self.hourIndex += newPosition
            # self.displayHours()
        if self.menuIndex == 2: # Load the minutes Menu options
            self.minuteIndex += newPosition
            # self.displayMinutes()
        self.setSelection(newPosition)

    def setSelection(self, direction):
        if self.selectionActive == True:
            self.dosomething()

    def displayDays(self):
        if self.dayIndex < 3:
            i = 0
            for block in self.listofVars:
                block.set(self.days[i])
                i += 1
        elif self.dayIndex >= 6:
            self.dayIndex = 6
            i = self.dayIndex - 3
            for block in self.listofVars:
                block.set(self.days[i])
                i += 1
        else:
            i = self.dayIndex - 2
            for block in self.listofVars:
                block.set(self.days[i])
                i += 1


    def updateSelectionMenu(self):
        # change the selection menu based on the current menuIndex
        if self.menuIndex == 0: #Set to days
            self.headingVar.set("Days Menu")
        elif self.menuIndex == 1:
            self.headingVar.set("Hours Menu")
        else:
            self.headingVar.set("Minutes Menu")
        self.selectMove(0)

    def  makeStaticLabel(self,frame, words): # Generate a static label
        return Label(frame, text=words, relief=RIDGE, width=18, height=1)

    def makeVarLabel(self, frame, variable): # Generate a label with text attached to variable
        return Label(frame, textvariable=variable, relief=SUNKEN, width=18, height=2)

    def menuMove(self, direction):
        if direction == "right":
            self.menuIndex += 1 # should get me 0-2?
            self.menuIndex %= 3
            self.clearMenu()
            self.menu[self.menuIndex].configure(state='active')
        else:
            self.menuIndex -= 1
            self.menuIndex %= 3
            self.clearMenu()
            self.menu[self.menuIndex].configure(state='active')

        self.menuSounds[self.menuIndex].play()
        self.updateSelectionMenu()

    def clearSelection(self):
        for child in self.selectionFrame.winfo_children():
            child.configure(state='normal')

    def clearMenu(self):
        for child in self.menuFrame.winfo_children():
            child.configure(state='normal')

    def leftPress(self, event):
        if self.selectionActive == False:
            self.menuMove("left")
        else:
            self.selectMove(-1)

    def rightPress(self, event):
        if self.selectionActive == False:
            self.menuMove("right")
        else:
            self.selectMove(1)
    def selectPress(self, event):
        if self.selectionActive == False: # enter the currently selected menu
            for child in self.menuFrame.winfo_children():
                child.configure(state='disabled')
            for child in self.selectionFrame.winfo_children():
                child.configure(state='normal')
            self.selectionActive = True
        else:
            for child in self.menuFrame.winfo_children():
                child.configure(state='normal')
            for child in self.selectionFrame.winfo_children():
                child.configure(state='disable')
            self.menu[self.menuIndex].configure(state='active')
            self.selectionActive = False




# Now the tin soldier is all wound up, so we set it upon its way.
root = Tk()
myApp = SetUp(root)
root.mainloop()