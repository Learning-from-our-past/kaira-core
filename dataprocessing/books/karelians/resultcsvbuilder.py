# -*- coding: utf-8 -*-
import ntpath
import csv
from abc import abstractmethod
from books.karelians.extractionkeys import KEYS

class ResultCsvBuilder():

    #TODO: POISTA SISÄISEN TOTETUKSEN FUNKTIOT SILLÄ NE VOIVAT VAPAASTI VAIHDELLA
    def __init__(self):
        pass

    @abstractmethod
    def openCsv(self, filepath):
        self.filepath = filepath
        self.filename = ntpath.basename(self.filepath)
        self._initCsv()
        self.karelianLocationsMax = 0
        self.otherLocationsMax = 0
        self.rowsofcsv = []


    def _initCsv(self):
        self.openedCsv = open(self.filepath, "w", newline='', encoding="utf-8")
        self.csvWriter = csv.writer(self.openedCsv, delimiter="&")


    def _writeCsvHeaders(self):
        headers = ["Surname", "first names", "original family", "birthday", "birthMonth", "birthYear", "birthLocation", "profession/status", "omakotitalo", "imagepath", "hasSpouse", "spouseName"]

        for i in range(0, self.karelianLocationsMax):
            headers = headers + ["karelianLocation" + str(i), "movedIn" + str(i), "movedOut" + str(i), "latitude" + str(i), "longitude" + str(i)]

        for i in range(0, self.otherLocationsMax):
            headers = headers + ["otherLocation" + str(i), "movedIn" + str(i), "movedOut" + str(i), "latitude" + str(i), "longitude" + str(i)]
        self.csvWriter.writerow(headers)

    def writeRow(self, dataDict):
        self.rowsofcsv.append(self._createRowFromDict(dataDict))



    #make a dict of row content divided based on the content
    def _createRowFromDict(self, persondatadict):
        row = {"regular" : [persondatadict[KEYS["surname"]].value, persondatadict[KEYS["firstnames"]].value,
               persondatadict[KEYS["origfamily"]].value, persondatadict[KEYS["birthDay"]].value,
               persondatadict[KEYS["birthMonth"]].value, persondatadict[KEYS["birthYear"]].value,
               persondatadict[KEYS["birthLocation"]].value, persondatadict[KEYS["profession"]].value,
               persondatadict[KEYS["omakotitalo"]].value, persondatadict[KEYS["imagepath"]].value,
               persondatadict[KEYS["spouse"]].value[KEYS["hasSpouse"]].value, persondatadict[KEYS["spouse"]].value[KEYS["spouseName"]].value,] }
        row["karelianLocations"] = self._addKarelianLocations(persondatadict)
        row["otherLocations"] = self._addOtherLocations(persondatadict)
        print(row)
        return row

    def _addKarelianLocations(self, persondatadict):
        lrow = []
        locations = persondatadict[KEYS["karelianlocations"]].value

        if len(locations) > self.karelianLocationsMax:
            print(len(locations))
            self.karelianLocationsMax = len(locations)

        for l in locations:
            lrow.append(l.value[KEYS["karelianlocation"]].value) #name of the place
            lrow.append(l.value["movedIn"].value) #year when moved in
            lrow.append(l.value["movedOut"].value) #year when moved out
            lrow.append(l.value[KEYS["kareliancoordinate"]].value["latitude"].value) #latitude
            lrow.append(l.value[KEYS["kareliancoordinate"]].value["longitude"].value) #latitude
            print(lrow)


        return lrow

    def _addOtherLocations(self, persondatadict):
        lrow = []
        locations = persondatadict[KEYS["otherlocations"]].value

        if len(locations) > self.otherLocationsMax:
            self.otherLocationsMax = len(locations)

        for l in locations:
            lrow.append(l.value[KEYS["otherlocation"]].value) #name of the place
            lrow.append(l.value["movedIn"].value) #year when moved in
            lrow.append(l.value["movedOut"].value) #year when moved out
            lrow.append(l.value[KEYS["othercoordinate"]].value["latitude"].value) #latitude
            lrow.append(l.value[KEYS["othercoordinate"]].value["longitude"].value) #latitude
        return lrow

    def _addSpouseDataToRow(self,row, persondatadict):
        pass

    def _createWifeRowFromDict(self, wife):
        pass

    def _writeToFile(self):
        self._writeCsvHeaders()
        for row in self.rowsofcsv:
            w = row["regular"] + row["karelianLocations"]
            diff = self.karelianLocationsMax*5 - len(row["karelianLocations"])
            if diff > 0:            #tasaa rivit lisäämällä tyhjää
                w = w + [""]*diff #5 is the number of cells per location
            w = w + row["otherLocations"]
            diff = self.otherLocationsMax*5 - len(row["otherLocations"])
            if diff > 0:            #tasaa rivit lisäämällä tyhjää
                w = w + [""]*diff
            self.csvWriter.writerow(w)

    @abstractmethod
    def closeCsv(self):
        print("closed")
        self._writeToFile()

        self.openedCsv.close()
        self.openedCsv = None