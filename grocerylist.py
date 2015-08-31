__author__ = 'Jason Maderski'
__date__ = '8-25-2015'
import time
import os.path
import re


class DateAndTime:

    getTimeAndDate = time.localtime()

    # Return year from current date
    def getYear(self):
        year = DateAndTime.getTimeAndDate[0]
        return year

    # Return month from current date
    def getMonth(self):
        month = DateAndTime.getTimeAndDate[1]
        return month

    # Return day from current date
    def getDay(self):
        day = DateAndTime.getTimeAndDate[2]
        return day

    # Return current date in a array
    def getDate(self):
        date = []
        date.append(self.getMonth())
        date.append(self.getDay())
        date.append(self.getYear())
        print date

    # Return Hour from current time
    def getHour(self):
        twentyFourHour = DateAndTime.getTimeAndDate[3]
        if twentyFourHour > 12:
            hour = twentyFourHour - 12
        else:
            hour = twentyFourHour
        return hour

    # Return minutes from current time
    def getMinutes(self):
        minutes = DateAndTime.getTimeAndDate[4]
        return minutes

    # Return seconds from current time
    def getSeconds(self):
        seconds = DateAndTime.getTimeAndDate[5]
        return seconds

    # Return 0 if AM and 1 if PM
    def getAMPM(self):
        twentyFourHour = DateAndTime.getTimeAndDate[3]
        if twentyFourHour < 12 or twentyFourHour == 24:
            AMPM = 0
        else:
            AMPM = 1
        return AMPM

    # Return time as an Array
    def getTime(self):
        lTime = []
        lTime.append(self.getHour())
        lTime.append(self.getMinutes())
        lTime.append(self.getSeconds())
        lTime.append(self.getAMPM())
        print lTime
        return lTime

    # Return date as a string in a readable format
    def dateAsString(self):
        sDate = str(self.getMonth()) + "-" + str(self.getDay()) + "-" + str(self.getYear())
        return sDate

    # Return time as a string in a readable format
    def timeAsString(self):
        if self.getAMPM() == 0:
            AMPM = "AM"
        else:
            AMPM = "PM"

        if self.getMinutes() <10:
            minutes = "0"+ str(self.getMinutes())
        else:
            minutes = str(self.getMinutes())
        sTime = str(self.getHour()) + ":" + minutes + " " + AMPM
        return sTime


class groceries:

    listName = ""
    groceryList = []

    # Ask user to input the name of the list
    def setNameOfList(self):
        groceries.listName = raw_input("Please enter a list name: ")

    # Ask user to add items to list until 'done' is typed
    def addItems(self):
        i = 0
        item = ""

        print "Please add items to your grocery list now!"
        print "When finished type 'done'"

        while item != "done":
            item = raw_input(str(i+1) + ": ")
            if item != "done":
                groceries.groceryList.append(item)
            i += 1

    # Checks if inputed item is on the grocery list
    def checkItemOnList(self, item):
        if item in groceries.groceryList:
            return True
        else:
            return False


class PreviousFileWithList:

    # Returns True if file is found
    def doesFileExist(self):
        t = DateAndTime()
        currentFileName = groceries.listName + "_" + t.dateAsString() + ".txt"
        return os.path.isfile(currentFileName)

    # Add a item from the old list to the new list if it is not on the new list
    def addOldlistItem(self, oldList):
        g = groceries()

        # Checks to see if item from previous list is on the new list, if not the item is added
        i = 0
        while i < len(oldList):
            item = oldList[i]
            if(g.checkItemOnList(item) == False):
                g.groceryList.append(item)
                print "Adding item " + item
            i += 1

    # Edit previous file
    def previousFileToList(self):
        t = DateAndTime()
        currentFileName = groceries.listName + "_" + t.dateAsString() + ".txt"
        oldList = []
        # Attempt to open file, if file is found then get items listed in file and put them in a list called 'oldList'
        try:
            inputFile = open(currentFileName, "r")
            print "File found"
            i = 1
            for line in inputFile:
                if line.startswith("   " + str(i)):
                    line = re.sub('[ .)\n]', '', line)
                    line = ''.join(i for i in line if not i.isdigit())
                    oldList.append(line)
                    i += 1
            print "Old List:"
            print oldList

            inputFile.close()
        except Exception, e:
            print e
            print "Creating File: " + currentFileName

        return oldList


class ListToFile:

    # Output grocery list to a file
    def outputToFile(self):
        t = DateAndTime()
        # Set Output File name
        outputFile = open(groceries.listName + "_" + t.dateAsString() + ".txt", "w")
        # Add timestamp to file
        outputFile.write("Created at: " + t.timeAsString() + "\n\n" + "Items to get:" + "\n" + "-------------" + "\n")
        i = 0
        # Add grocery list items to file
        while i < len(groceries.groceryList):
            outputFile.write("   " +str(i+1) + ".) " + groceries.groceryList[i])
            outputFile.write("\n")
            i += 1
        # Stop Writing to File
        outputFile.close()


class main():
    def __init__(self):
        pass

    def start(self):

        t = DateAndTime()
        p = PreviousFileWithList()
        g = groceries()
        l = ListToFile()

        # Print time in console
        print "Time is: " + t.timeAsString()

        # Ask user for name of the list
        g.setNameOfList()

        # Ask user to add grocery items
        g.addItems()

        # Check to see if file exists, if so
        if p.doesFileExist():
            oldList = p.previousFileToList()
            p.addOldlistItem(oldList)

        # Print grocerylist information in console
        print "\n" + "Please Open file: " + groceries.listName + "_" + t.dateAsString() + "\n"
        print "List name: " + groceries.listName
        print "Date: " + t.dateAsString()
        print "Groceries on list: "
        print groceries.groceryList

        # Output grocery list to File
        l.outputToFile()

m = main()
m.start()

