__author__ = 'ReverendCode'

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
        self.selectionPosition = 0 # 0-3

        self.positions = [self.dayIndex, self.hourIndex, self.minuteIndex]
        self.maximums = [6,23,59]

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

    def selectActive(self, current, max, left):
        # This should return the location of the label to be highlighted
        if current == max:
            return 3
        if current == 0:
            return 0
        if current == 1:
            return 1
        if current == max-1:
            return 2
        if left:
            return 1
        else:
            return 2

    def constructSelections(self, position, current, menu):
        # This should set the text in the lower menu to the correct values, based on the position in the menu
        start = current-position
        if menu == 0: # You are in the 'Days' menu
            for var in self.listofVars:
                var.set(self.days[start])
                start += 1
        elif menu == 1: # This is hours
            for var in self.listofVars:
                if start < 11:
                    start +=1
                    var.set(str(start) + "AM")
                elif start >= 11 & start < 23:
                    start +=1
                    var.set(str(start-12) + "PM")

                elif start > 23:
                    start = 1
                    var.set(start + "AM")

        else:  # This should be minutes
            for var in self.listofVars:
                if start > 59:
                    start = 0
                var.set(start)
                start +=1

    def activate(self,position):
        self.clearSelection()
        if position == 0:
            self.labelLL.configure(state='active')
        elif position == 1:
            self.labelL.configure(state='active')
        elif position == 2:
            self.labelR.configure(state='active')
        else:
            self.labelRR.configure(state='active')

    def rightPress(self, event):
        if self.selectionActive == False:
            self.menuMove("right")
            self.constructSelections(self.selectionPosition, self.positions[self.menuIndex], self.menuIndex)
        else:
            maxx = self.maximums[self.menuIndex]
            self.positions[self.menuIndex] += 1
            self.positions[self.menuIndex] %= maxx+1
            posit = self.positions[self.menuIndex]
            print(str(posit)+" is the correct position")
            self.selectionPosition = self.selectActive(posit, maxx, False)
            print(str(self.selectionPosition)+"is the location of the selected position")
            self.constructSelections(self.selectionPosition, posit,self.menuIndex)
            self.activate(self.selectionPosition)



    def leftPress(self, event):
        if self.selectionActive == False:
            self.menuMove("left")
            self.constructSelections(self.selectionPosition,self.positions[self.menuIndex],self.menuIndex)
        else:
            maxx = self.maximums[self.menuIndex]
            self.positions[self.menuIndex] -= 1
            self.positions[self.menuIndex] %= maxx+1
            posit = self.positions[self.menuIndex]
            self.selectionPosition = self.selectActive(posit, maxx,True)
            self.constructSelections(self.selectionPosition, posit,self.menuIndex)
            self.activate(self.selectionPosition)


    def selectPress(self, event):
        if self.selectionActive == False:
            self.setChildren('disabled',self.menuFrame)
            self.setChildren('normal',self.selectionFrame)
            self.selectionPosition = self.selectActive(self.positions[self.menuIndex],self.maximums[self.menuIndex],False)
            self.constructSelections(self.selectionPosition,self.positions[self.menuIndex],self.menuIndex)
            self.activate(self.selectionPosition)
            self.selectionActive = True
        else:
            self.setChildren('normal', self.menuFrame)
            self.setChildren('disabled',self.selectionFrame)
            self.selectionActive = False

    def setChildren(self, state, frame):
        for child in frame.winfo_children():
            child.configure(state=state)

    # Some basic helper functions live here.
    def clearSelection(self):
        for child in self.selectionFrame.winfo_children():
            child.configure(state='normal')

    def clearMenu(self):
        for child in self.menuFrame.winfo_children():
            child.configure(state='normal')


    def  makeStaticLabel(self,frame, words): # Generate a static label
        return Label(frame, text=words, relief=RIDGE, width=18, height=1)

    def makeVarLabel(self, frame, variable): # Generate a label with text attached to variable
        return Label(frame, textvariable=variable, relief=SUNKEN, width=18, height=2)



# Now the tin soldier is all wound up, so we set it upon its way.
root = Tk()
myApp = SetUp(root)
root.mainloop()