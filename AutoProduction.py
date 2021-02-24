import tarfile
import csv
from subprocess import Popen, PIPE
import time


STANDARD_CSV_FILE_NAME        = "Higher_mass_fD_autoProduction.csv"
STANDARD_PARAM_CARD_FILE_NAME = "param_card.dat"

#function below checks to see if a file exists and yells and quits if it doesn't exist
def fileExists(fileName):
    try:
        return open(fileName, 'r+')
    except:
        print("File specified: \"" + str(fileName) + "\" not found. make sure file exists and try again")
        quit()

#function below will check and change the ParamCard
def changeParamCard(MZd, MFd1, paramCardFileName):
    #gets the fileReader via fileExists
    massiveFileString = "";
    with fileExists(paramCardFileName) as fp:
        line = fp.readline()
        while line:
            if "MZd" in line or "MFd1" in line:
                #separates each line based on whitespace
                lineArr = line.split(" ")

                #removes any null string characters
                lineArr = [i for i in lineArr if i != '']

                #sets designated number
                setNumber = 0
                setString = ""
                if "MZd" in line:
                    number = MZd
                    setString = "MZd"
                else:
                    number = MFd1
                    setString = "MFd1"

                #makes a new line and adds that to the massiveFileString
                newLine = lineArr[0] + " " + str("{:.6e}".format(number)) + " # " + setString + "\n"
                massiveFileString += newLine
            #appends generic string to line to write later on
            else:
                massiveFileString += line
            
            line = fp.readline()

    with open(paramCardFileName, 'w') as fp:
        fp.write(massiveFileString)
    


#function that gets CSVInformation from standard set CSV's created
def getCSVInformation(csvFileName):
    #below gets the tempreader via the fileExists function.
    tempFile = fileExists(csvFileName)
    tempReader = tempFile.read(1024)

    #dialect is found here, and then 
    dialect = csv.Sniffer().sniff(tempReader)
    csvFile = open(csvFileName, 'r')
    csvReader = csv.reader(csvFile, dialect)

    #variables declared below are to be used in upcoming loop through csv
    itemDictionary = {}
    start = []
    end = []

    #goes through each rwo in the csv and starts organizing data 
    for row in csvReader:
        if (row[0] == "MZd"):
            for item in row:
                if (item != "MZd"):
                    itemDictionary.update({item : []})
        elif row[0] == "MfD1":
            for item in row:
                if(item != "MfD1"):
                    start.append(item)
        elif row[0] == "":
            for item in row:
                if (item != ""):
                    end.append(item)
        else:
            print("csvfile you input is in wrong format. Try again")
            quit()

    #goes through each item in the dictionary and gets the start and end range and appends that to the dictionary.      
    count = 0
    for key in itemDictionary:
        try:
            itemDictionary[key] = [x for x in range(int(start[count]), int(end[count])) if x % 5 == 0]
            count+=1
        except:
            input("do not have enough items in start or end. try again")
            exit()

    #print("Dictionary is:\n" + str(itemDictionary))

    #closes all the files so nothing weird and obscure happens
    csvFile.close()
    tempFile.close()

    #return dictionary
    return itemDictionary

#below is where the filepath is stored, this is where you change the filepath

informationDictionary = getCSVInformation(STANDARD_CSV_FILE_NAME)

for mzdItem in informationDictionary:
    for mfd1Item in informationDictionary.get(mzdItem):
        changeParamCard(int(mzdItem), int(mfd1Item),STANDARD_PARAM_CARD_FILE_NAME)
        #run command
        p = Popen("./bin/generate_events",stdin=PIPE, shell=True)
        time.sleep(5)
        p.communicate(input=b'\n')
        time.sleep(5)
        p.communicate
        time.sleep(120)
        #Events/run*
        #foreach run:
        #find gz, untar, and store
        #mkdir under specific MZD mass, and then rezip in events
        #untar a file and put it in some other directory

#after untarring everything and storing in a director retar everything


