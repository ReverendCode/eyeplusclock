__author__ = 'ReverendCode'
#comments in python use the pound thingy
from tkinter import *

class SetUp: #Prepare the canvas
    def __init__(self, parent):
        self.myParent = parent
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

        self.menuLabel1 = self.makeLabel(self.menuFrame, "Main Menu")
        self.menuLabel1.pack(side = LEFT)
        self.menuLabelSpace = Label(self.menuFrame, width = 2)
        self.menuLabelSpace.pack(side = LEFT)
        words = "Set Day"
        self.menuLabel2 = self.makeLabel(self.menuFrame, "Set Day")
        self.menuLabel2.pack(side = LEFT)
        self.menuLabel3 = self.makeLabel(self.menuFrame, "Set Hour")
        self.menuLabel3.pack(side = LEFT)
        self.menuLabel4 = self.makeLabel(self.menuFrame, "Set Minute")
        self.menuLabel4.pack(side=LEFT)

        self.selectionFrame = Frame(self.rootContainer)
        self.selectionFrame.pack(side=TOP)


        # have I mentioned how much I like indices?
        self.menuIndex = 0
        self.dayIndex = 0
        self.hourIndex = 0
        self.minuteIndex = 0

    def makeLabel(self,frame, words):
        return Label(frame, text = words, relief = RIDGE, width = 18, height = 1)


# Now the tin soldier is all wound up, so we set it upon its way.
root = Tk()
myApp = SetUp(root)
root.mainloop()