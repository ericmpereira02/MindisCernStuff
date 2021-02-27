import tarfile, csv, sys
from subprocess import Popen, PIPE
import os
from shutil import rmtree as rmtree
from time import sleep as sleep

#THESE ARE ALL RELATIVE LOCATIONS
STANDARD_CSV_FILE_NAME        = "Higher_mass_fD_autoProduction.csv"
STANDARD_PARAM_CARD_FILE_NAME = "param_card.dat"
EVENTS_DIRECTORY              = "../Events"
GENERATE_EVENTS               = "./../bin/generate"

#function below checks to see if a file exists and yells and quits if it doesn't exist
def fileExists(fileName):
    try:
        return open(fileName, 'r+')
    except Exception as e:
        print(e + "\n\nFile specified: \"" + str(fileName) + "\" not found. make sure file exists and try again")
        exit()

#function below will check and change the ParamCard
def changeParamCard(MZd, MFd1, paramCardFileName):
    #gets the fileReader via fileExists
    massiveFileString = "";
    with fileExists(paramCardFileName) as fp:
        line = fp.readline()
        while line:
            if 'MZd' in line or 'MFd1' in line:
                #separates each line based on whitespace
                lineArr = line.split(' ')

                #removes any null string characters
                lineArr = [i for i in lineArr if i != '']

                #sets designated number
                setNumber = 0
                setString = ''
                if 'MZd' in line:
                    number = MZd
                    setString = 'MZd'
                else:
                    number = MFd1
                    setString = 'MFd1'

                #makes a new line and adds that to the massiveFileString
                newLine = lineArr[0] + ' ' + str('{:.6e}'.format(number)) + ' # ' + setString + '\n'
                massiveFileString += newLine
            #appends generic string to line to write later on
            else:
                massiveFileString += line

            #reads the next line to continue loop
            line = fp.readline()

    #opens the paramCardFile and completely writes over everything with data just compiled
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
        if (row[0] == 'MZd'):
            for item in row:
                if (item != 'MZd'):
                    itemDictionary.update({item : []})
        elif row[0] == 'MfD1':
            for item in row:
                if(item != 'MfD1'):
                    start.append(item)
        elif row[0] == '':
            for item in row:
                if (item != ""):
                    end.append(item)
        #throws an error in the csv is in the wrong format
        else:
            print('csvfile you input is in wrong format. Try again')
            exit()

    #goes through each item in the dictionary and gets the start and end range and appends that to the dictionary.      
    count = 0
    for key in itemDictionary:
        try:
            itemDictionary[key] = [x for x in range(int(start[count]), int(end[count])) if x % 5 == 0]
            count+=1
        except Exception as e:
            print(e + '\n\ndo not have enough items in start or end. try again')
            exit()

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
        eventListBefore = os.listdir(EVENTS_DIRECTORY)
        #This Try except will try to run the event, if it fails it will print error and quit
        try:
            # a sleep is implemented between each event generation as 
            p = Popen(GENERATE_EVENTS,stdin=PIPE, shell=True)
            sleep(5)
            p.communicate(input=b'\n')
            sleep(5)
            p.communicate
            sleep(300)
        except:
            print(GENERATE_EVENTS + ' is not found, try changing path and going again')
            #exit()
        #goes through events directory to find the runs
        print("mzd: " + str(mzdItem) + ", mfd: " + str(mfd1Item))
        sleep(5)
        eventListAfter = os.listdir(EVENTS_DIRECTORY)
        item = [i for i in eventListAfter if i not in eventListBefore]
        for event in item:
            if 'run' in event:
                runDirList = os.listdir(EVENTS_DIRECTORY+'/'+event)
                for runItem in runDirList:
                    if runItem[-2:] == 'gz':
                        #opens the tarred file, and untars it in specified location under specific mzd and mfd
                        with tarfile.open(EVENTS_DIRECTORY+'/'+event+'/'+runItem) as eventTar:
                            try:
                                eventTar.extractall(path=(EVENTS_DIRECTORY+'/mzd_'+str(mzdItem)+'/mfd1_'+str(mfd1Item)))
                                rmtree(EVENTS_DIRECTORY+'/'+event)
                            except Exception as e:
                                print(e + '\n\nfile: ' + (EVENTS_DIRECTORY+'/'+event+'/'+runItem) + ' is unable to be untarred')
                                exit()
                        try:
                            currentDirectory = os.getcwd()
                            os.chdir(EVENTS_DIRECTORY)
                            tarName = 'mzd_' + str(mzdItem)+'.tar.gz'
                            with tarfile.open(tarName, 'w:gz') as tar:
                                stuff = tar.add('mzd_'+str(mzdItem)+'/mfd1_'+str(mfd1Item))
                                rmtree('mzd_'+str(mzdItem))
                                os.chdir(currentDirectory)
                        except Exception as e:
                            os.chdir(currentDirectory)
                            print(e + '\n\nUnable to compress file, continuing...')


