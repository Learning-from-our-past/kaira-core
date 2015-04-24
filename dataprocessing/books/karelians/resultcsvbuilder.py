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


    def _initCsv(self):
        self.openedCsv = open(self.filepath, "w", newline='', encoding="utf-8")
        self.csvWriter = csv.writer(self.openedCsv, delimiter="&")
        self._writeCsvHeaders()

    def _writeCsvHeaders(self):
        self.csvWriter.writerow(["Surname", "first names", "original family", "birthday", "birthMonth", "birthYear", "birthLocation", "profession/status", "karelian locations", "omakotitalo", "imagepath"])


    def writeRow(self, dataDict):
        row = self._createRowFromDict(dataDict)
        self.csvWriter.writerow(row)

    #TODO: THIS REQUIRES MORE SENSIBLE SOLUTION!
    #tranforms the dict of the entry to a format which can be written into csv
    def _createRowFromDict(self, persondatadict):
        row = [persondatadict[KEYS["surname"]].value, persondatadict[KEYS["firstnames"]].value,
               persondatadict[KEYS["origfamily"]].value, persondatadict[KEYS["birthDay"]].value,
               persondatadict[KEYS["birthMonth"]].value, persondatadict[KEYS["birthYear"]].value,
               persondatadict[KEYS["birthLocation"]].value, persondatadict[KEYS["profession"]].value,
               persondatadict[KEYS["karelianlocations"]].value,
               persondatadict[KEYS["omakotitalo"]].value, persondatadict[KEYS["imagepath"]].value,]
        self._addKarelianLocations(persondatadict)
        return row

    def _addKarelianLocations(self, persondatadict):
        lrow = []
        locations = persondatadict[KEYS["karelianlocations"]].value

        for l in locations:
            lrow.append(l.value[KEYS["karelianlocation"]].value) #name of the place
            lrow.append(l.value["movedIn"].value) #year when moved in
            lrow.append(l.value["movedOut"].value) #year when moved out
            lrow.append(l.value[KEYS["kareliancoordinate"]].value["latitude"].value) #latitude
            lrow.append(l.value[KEYS["kareliancoordinate"]].value["longitude"].value) #latitude
            print(lrow)

        print("asdasdsasd")
        print(lrow)

    def _addSpouseDataToRow(self,row, persondatadict):
        pass

    def _createWifeRowFromDict(self, wife):
        pass

    @abstractmethod
    def closeCsv(self):
        self.openedCsv.close()
        self.openedCsv = None