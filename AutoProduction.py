import tarfile
import csv
import sys
import os

#below is where the filepath is stored, this is where you change the filepath
csvFileName = "Higher_mass_fD_autoProduction.csv";
print("filepath is: " + str(csvFileName))

#the csvfile is temporarily opened in order to get the proper dialect
try:
    csvFile = open(csvFileName)
    tempReader = csvFile.read(1024)
except:
    print("csv file input not found. Try Again")
    quit()

#dialect is found here, and then 
dialect = csv.Sniffer().sniff(tempReader)
csvFile = open(csvFileName)
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

print(itemDictionary)
