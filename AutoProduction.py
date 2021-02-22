import tarfile
import csv
import sys
import os

filePath = "C:\\Higher_mass_fD_autoProduction.csv";
print(str(filePath))

csvFile = open(filePath)
csvReader = csvFile.read(1024)
print(csvReader)

dialect = csv.Sniffer().sniff(csvReader)
reader = csv.reader(csvFile, dialect)

for row in reader:
    print("inside")
    print(row)

with open(csvFile) as someCSV:
    dialect = csv.Sniffer().sniff(csvReader)
    someCSV.seek(0)
    reader = csv.reader(someCSV, dialect)

input("fuckem bois")

start = []
end = []
with open (file, mode='r') as csv_file:
    for row in data:
        print(row)
        if (row[0] == "MZd"):
            for item in row:
                itemDictionary.update({item : []})
        elif row[0] == "MfD1":
            for item in row:
                start.append(item)
        elif row[0] == "":
            for item in row:
                end.append(item)
        else:
            input("csvfile you input is in wrong format. Try again")

    count = 0
    for key in itemDictionary:
        try:
            itemDictionary[key] = [x for x in range(start[count], end[x]) if x % 5 == 0]
            count+=1
        except:
            input("do not have enough items in start or end. try again")
            exit()
