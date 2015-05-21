# -*- coding: utf-8 -*-
import ntpath
import csv
import json
from abc import abstractmethod
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from interface.csvbuilderinterface import ResultCsvBuilderInterface

class ResultCsvBuilder(ResultCsvBuilderInterface):

    #TODO: POISTA SISÄISEN TOTETUKSEN FUNKTIOT SILLÄ NE VOIVAT VAPAASTI VAIHDELLA
    def __init__(self):
        pass

    @abstractmethod
    def openCsv(self, filepath):
        self.filepath = filepath
        self.filename = ntpath.basename(self.filepath)
        self._initCsv()
        self.childrenMax = 0
        self.rowsofcsv = []


    def _initCsv(self):
        self.openedCsv = open(self.filepath, "w", newline='', encoding="utf-8")
        self.csvWriter = csv.writer(self.openedCsv, delimiter="&")


    def _writeCsvHeaders(self):
        headers = ["FarmName", "FarmLocation", "FarmLatitude", "FarmLongitude", "Owner first names", "Owner surname", "Owner gender", "OwnerBirthday", "OwnerBirthMonth", "OwnerBirthYear", "ownerSince", "Hostess first names", "Hostess surname", "HostessGender", "HostessBirthday", "HostessBirthMonth", "HostessBirthYear", "approximatePageNumber", "maybeManyMarriages" ]

        headers = headers + ["ChildCount"]
        for i in range(0, self.childrenMax):
            headers = headers + ["Child" + str(i), "Gender" + str(i), "ChildBirthYear" + str(i)]


        self.csvWriter.writerow(headers)

    def writeRow(self, dataDict):
        self.rowsofcsv.append(self._createRowFromDict(dataDict))

    #make a dict of row content divided based on the content
    def _createRowFromDict(self, persondatadict):
        row = {"regular" : [persondatadict[KEYS["name"]].value,
                            persondatadict[KEYS["farmLocation"]].value["locationName"].value,
                            persondatadict[KEYS["farmLocation"]].value["latitude"].value,
                            persondatadict[KEYS["farmLocation"]].value["longitude"].value,
                            persondatadict[KEYS["owner"]].value[KEYS["firstnames"]].value,
                            persondatadict[KEYS["owner"]].value[KEYS["surname"]].value,
                            persondatadict[KEYS["owner"]].value[KEYS["gender"]].value,
                            persondatadict[KEYS["owner"]].value[KEYS["ownerBirthData"]].value[KEYS["birthDay"]].value,
                            persondatadict[KEYS["owner"]].value[KEYS["ownerBirthData"]].value[KEYS["birthMonth"]].value,
                            persondatadict[KEYS["owner"]].value[KEYS["ownerBirthData"]].value[KEYS["birthYear"]].value,
                            persondatadict[KEYS["owner"]].value[KEYS["ownerFrom"]].value,

                            persondatadict[KEYS["hostess"]].value[KEYS["firstnames"]].value,
                            persondatadict[KEYS["hostess"]].value[KEYS["surname"]].value,
                            persondatadict[KEYS["hostess"]].value[KEYS["gender"]].value,
                            persondatadict[KEYS["hostess"]].value[KEYS["hostessBirthData"]].value[KEYS["birthDay"]].value,
                            persondatadict[KEYS["hostess"]].value[KEYS["hostessBirthData"]].value[KEYS["birthMonth"]].value,
                            persondatadict[KEYS["hostess"]].value[KEYS["hostessBirthData"]].value[KEYS["birthYear"]].value,
                            persondatadict[KEYS["approximatePage"]].value,
                            persondatadict[KEYS["manymarriages"]].value



               ] }
        row["children"] = self._addChildren(persondatadict)
        return row


    def _addChildren(self, persondatadict):
        lrow = []
        children = persondatadict[KEYS["children"]].value

        #childcount
        lrow.append(persondatadict[KEYS["childCount"]].value)

        if len(children) > self.childrenMax:
            self.childrenMax = len(children)

        for l in children:
            lrow.append(l.value["name"].value) #name of the child
            lrow.append(l.value["gender"].value)
            lrow.append(l.value["birthYear"].value) #child's birthYear
        return lrow

    def _writeToFile(self):
        self._writeCsvHeaders()
        for row in self.rowsofcsv:
            w = row["regular"] + row["children"]
            diff = self.childrenMax*3 - len(row["children"]) +1   #1 for childrencount column
            if diff > 0:            #tasaa rivit lisäämällä tyhjää
                w = w + [""]*diff #3 is the number of cells per child

            self.csvWriter.writerow(w)

    @abstractmethod
    def closeCsv(self):
        self._writeToFile()
        self.openedCsv.close()
        self.openedCsv = None