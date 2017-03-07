# -*- coding: utf-8 -*-
import ntpath
import csv
from abc import abstractmethod
from book_extractors.karelians.extractionkeys import KEYS
from interface.csvbuilderinterface import ResultCsvBuilderInterface

# FIXME: Rewrite this class. Out of date.
class ResultCsvBuilder(ResultCsvBuilderInterface):

    def __init__(self):
        pass

    @abstractmethod
    def openCsv(self, file):
        self.karelianLocationsMax = 0
        self.childrenMax = 0
        self.otherLocationsMax = 0
        self.rowsofcsv = []

        if type(file) == str:
            self.openedCsv = open(file, "w", newline='', encoding="utf-8")
        else:
            self.openedCsv = file

        self.csvWriter = csv.writer(self.openedCsv, delimiter="&")

    def _writeCsvHeaders(self):
        headers = ["Surname", "first names", "gender", "original family", "birthday", "birthMonth", "birthYear", "birthLocation", "profession/status", "omakotitalo", "imagepath", "approximatePageNumber", "returnedToKarelia", "hasSpouse", "maybePreviousMarriages", "weddingYear", "spouseName", "spouseOrigFamily", "spouseProfession", "spouseBirthday", "spouseBirthMonth", "spouseBirthYear", "spouseBirthLocation", "spouseDeathYear" ]

        headers = headers + ["ChildCount", "BoyCount", "GirlCount"]
        for i in range(0, self.childrenMax):
            headers = headers + ["Child" + str(i), "Gender" + str(i), "ChildBirthYear" + str(i), "childBirthLocation" + str(i), "childBirthLatitude" + str(i), "childBirthLongitude" + str(i)]


        headers = headers + [KEYS["karelianlocationsCount"]]
        for i in range(0, self.karelianLocationsMax):
            headers = headers + ["karelianLocation" + str(i), "movedIn" + str(i), "movedOut" + str(i), "latitude" + str(i), "longitude" + str(i)]

        headers = headers + [KEYS["otherlocationsCount"]]
        for i in range(0, self.otherLocationsMax):
            headers = headers + ["otherLocation" + str(i), "movedIn" + str(i), "movedOut" + str(i), "latitude" + str(i), "longitude" + str(i)]
        self.csvWriter.writerow(headers)

    def writeRow(self, dataDict):
        self.rowsofcsv.append(self._createRowFromDict(dataDict))

    #make a dict of row content divided based on the content
    def _createRowFromDict(self, persondatadict):
        row = {"regular" : [persondatadict[KEYS["surname"]],
                            persondatadict[KEYS["firstnames"]],persondatadict[KEYS["gender"]],
               persondatadict[KEYS["origfamily"]], persondatadict[KEYS["birthDay"]],
               persondatadict[KEYS["birthMonth"]], persondatadict[KEYS["birthYear"]],
               persondatadict[KEYS["birthLocation"]], persondatadict[KEYS["profession"]],
               persondatadict[KEYS["omakotitalo"]], persondatadict[KEYS["imagepath"]], persondatadict[KEYS["approximatePage"]],
               persondatadict[KEYS["returnedkarelia"]],
               persondatadict[KEYS["spouse"]][KEYS["hasSpouse"]],
               persondatadict[KEYS["manymarriages"]],
               persondatadict[KEYS["spouse"]][KEYS["weddingYear"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseName"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseOrigFamily"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseProfession"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseBirthData"]][KEYS["birthDay"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseBirthData"]][KEYS["birthMonth"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseBirthData"]][KEYS["birthYear"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseBirthData"]][KEYS["birthLocation"]],
               persondatadict[KEYS["spouse"]][KEYS["spouseDeathYear"]],

               ] }
        row["children"] = self._addChildren(persondatadict)
        row["karelianLocations"] = self._addKarelianLocations(persondatadict)
        row["otherLocations"] = self._addOtherLocations(persondatadict)

        return row


    def _addChildren(self, persondatadict):
        lrow = []
        children = persondatadict[KEYS["children"]]

        #childcount
        lrow.append(persondatadict[KEYS["childCount"]])
        lrow.append(persondatadict[KEYS["boyCount"]])
        lrow.append(persondatadict[KEYS["girlCount"]])

        if len(children) > self.childrenMax:
            self.childrenMax = len(children)

        for l in children:
            lrow.append(l["name"]) #name of the child
            lrow.append(l["gender"])
            lrow.append(l["birthYear"]) #child's birthYear
            lrow.append(l["locationName"]) #birthplace
            lrow.append(l["childCoordinates"]["latitude"]) #latitude
            lrow.append(l["childCoordinates"]["longitude"]) #latitude
        return lrow




    def _addKarelianLocations(self, persondatadict):
        lrow = []
        locations = persondatadict[KEYS["karelianlocations"]]

        #location count
        lrow.append(persondatadict[KEYS["karelianlocationsCount"]])

        if len(locations) > self.karelianLocationsMax:
            self.karelianLocationsMax = len(locations)

        for l in locations:
            lrow.append(l[KEYS["karelianlocation"]]) #name of the place
            lrow.append(l["movedIn"]) #year when moved in
            lrow.append(l["movedOut"]) #year when moved out
            lrow.append(l[KEYS["kareliancoordinate"]]["latitude"]) #latitude
            lrow.append(l[KEYS["kareliancoordinate"]]["longitude"]) #latitude



        return lrow

    def _addOtherLocations(self, persondatadict):
        lrow = []
        locations = persondatadict[KEYS["otherlocations"]]

        #location count
        lrow.append(persondatadict[KEYS["otherlocationsCount"]])

        if len(locations) > self.otherLocationsMax:
            self.otherLocationsMax = len(locations)

        for l in locations:
            lrow.append(l[KEYS["otherlocation"]]) #name of the place
            lrow.append(l["movedIn"]) #year when moved in
            lrow.append(l["movedOut"]) #year when moved out
            lrow.append(l[KEYS["othercoordinate"]]["latitude"]) #latitude
            lrow.append(l[KEYS["othercoordinate"]]["longitude"]) #latitude


        return lrow


    def _writeToFile(self):
        self._writeCsvHeaders()
        for row in self.rowsofcsv:

            w = row["regular"] + row["children"]
            diff = self.childrenMax*6 - len(row["children"]) +3   #3 for childrencount columns
            if diff > 0:            #tasaa rivit lisäämällä tyhjää
                w = w + [""]*diff #6 is the number of cells per child

            w = w + row["karelianLocations"]
            diff = self.karelianLocationsMax*5 - len(row["karelianLocations"]) +1   #1 for locationcount column
            if diff > 0:            #tasaa rivit lisäämällä tyhjää
                w = w + [""]*diff

            w = w + row["otherLocations"]
            diff = self.otherLocationsMax*5 - len(row["otherLocations"]) +1 #1 for locationcount column
            if diff > 0:            #tasaa rivit lisäämällä tyhjää
                w = w + [""]*diff
            self.csvWriter.writerow(w)

    @abstractmethod
    def closeCsv(self):
        self._writeToFile()
        self.openedCsv.close()
        self.openedCsv = None
