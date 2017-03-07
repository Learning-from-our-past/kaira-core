# -*- coding: utf-8 -*-
import ntpath
import csv
from abc import abstractmethod
from book_extractors.common.extraction_keys import KEYS
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
        headers = ["FarmName", "FarmLocation", "FarmLatitude", "FarmLongitude", "FarmArea ha", "ForestArea ha", "FieldArea ha", "WasteArea ha", "MeadowArea ha", "Owner first names", "Owner surname", "Owner gender", "OwnerBirthday", "OwnerBirthMonth", "OwnerBirthYear", "ownerSince"]
        headers = headers + ["oat", "barley", "hay", "potatoes", "wheat", "rye", "sugarbeet", "lanttu", "puimakone", "tractor", "horse", "chicken", "siirtotila", "kantatila",
                             "talli", "sauna", "navetta", "autotalli", "lypsykone", "pine", "spruce", "birch", "someoneDead",
                             "moreeni", "hiesu", "hieta", "muta", "savi", "multa", "salaojitus",
                             "rooms", "lypsylehmät", "teuraseläimet", "lampaat", "lihotussiat", "emakot", "nuori",
                             "kanat"]

        headers = headers + ["Hostess first names", "Hostess surname", "HostessGender", "HostessBirthday", "HostessBirthMonth", "HostessBirthYear", "approximatePageNumber", "maybeManyMarriages"]

        headers = headers + ["ChildCount", "BoyCount", "GirlCount"]
        for i in range(0, self.childrenMax):
            headers = headers + ["Child" + str(i), "Gender" + str(i), "ChildBirthYear" + str(i)]


        self.csvWriter.writerow(headers)

    def writeRow(self, dataDict):
        self.rowsofcsv.append(self._createRowFromDict(dataDict))

    #make a dict of row content divided based on the content
    def _createRowFromDict(self, persondatadict):
        row = {"regular" : [persondatadict[KEYS["name"]],

                            persondatadict[KEYS["farmLocation"]]["locationName"],
                            persondatadict[KEYS["farmLocation"]]["latitude"],
                            persondatadict[KEYS["farmLocation"]]["longitude"],

                            persondatadict[KEYS["farmDetails"]][KEYS["wholeArea"]],
                            persondatadict[KEYS["farmDetails"]][KEYS["forestArea"]],
                            persondatadict[KEYS["farmDetails"]][KEYS["fieldArea"]],
                            persondatadict[KEYS["farmDetails"]][KEYS["wasteArea"]],
                            persondatadict[KEYS["farmDetails"]][KEYS["meadowArea"]],

                            persondatadict[KEYS["owner"]][KEYS["firstnames"]],
                            persondatadict[KEYS["owner"]][KEYS["surname"]],
                            persondatadict[KEYS["owner"]][KEYS["gender"]],
                            persondatadict[KEYS["owner"]][KEYS["ownerBirthData"]][KEYS["birthDay"]],
                            persondatadict[KEYS["owner"]][KEYS["ownerBirthData"]][KEYS["birthMonth"]],
                            persondatadict[KEYS["owner"]][KEYS["ownerBirthData"]][KEYS["birthYear"]],
                            persondatadict[KEYS["owner"]][KEYS["ownerFrom"]],

                            persondatadict[KEYS["flags"]][KEYS["oat"]],
                            persondatadict[KEYS["flags"]][KEYS["barley"]],
                            persondatadict[KEYS["flags"]][KEYS["hay"]],
                            persondatadict[KEYS["flags"]][KEYS["potatoes"]],
                            persondatadict[KEYS["flags"]][KEYS["wheat"]],
                            persondatadict[KEYS["flags"]][KEYS["rye"]],
                            persondatadict[KEYS["flags"]][KEYS["sugarbeet"]],
                            persondatadict[KEYS["flags"]][KEYS["lanttu"]],

                            persondatadict[KEYS["flags"]][KEYS["puimakone"]],
                            persondatadict[KEYS["flags"]][KEYS["tractor"]],
                            persondatadict[KEYS["flags"]][KEYS["horse"]],
                            persondatadict[KEYS["flags"]][KEYS["chicken"]],
                            persondatadict[KEYS["flags"]][KEYS["siirtotila"]],
                            persondatadict[KEYS["flags"]][KEYS["kantatila"]],

                            persondatadict[KEYS["flags"]][KEYS["talli"]],
                            persondatadict[KEYS["flags"]][KEYS["sauna"]],
                            persondatadict[KEYS["flags"]][KEYS["navetta"]],
                            persondatadict[KEYS["flags"]][KEYS["autotalli"]],
                            persondatadict[KEYS["flags"]][KEYS["lypsykone"]],
                            persondatadict[KEYS["flags"]][KEYS["pine"]],
                            persondatadict[KEYS["flags"]][KEYS["spruce"]],
                            persondatadict[KEYS["flags"]][KEYS["birch"]],
                            persondatadict[KEYS["flags"]][KEYS["someonedead"]],


                            persondatadict[KEYS["flags"]][KEYS["moreeni"]],
                            persondatadict[KEYS["flags"]][KEYS["hiesu"]],
                            persondatadict[KEYS["flags"]][KEYS["hieta"]],
                            persondatadict[KEYS["flags"]][KEYS["muta"]],
                            persondatadict[KEYS["flags"]][KEYS["savi"]],
                            persondatadict[KEYS["flags"]][KEYS["multa"]],
                            persondatadict[KEYS["flags"]][KEYS["salaojitus"]],

                            persondatadict[KEYS["quantities"]][KEYS["rooms"]],
                            persondatadict[KEYS["quantities"]][KEYS["lypsylehma"]],
                            persondatadict[KEYS["quantities"]][KEYS["teuras"]],
                            persondatadict[KEYS["quantities"]][KEYS["lammas"]],
                            persondatadict[KEYS["quantities"]][KEYS["lihotussika"]],
                            persondatadict[KEYS["quantities"]][KEYS["emakko"]],
                            persondatadict[KEYS["quantities"]][KEYS["nuori"]],
                            persondatadict[KEYS["quantities"]][KEYS["kanoja"]],

                            persondatadict[KEYS["hostess"]][KEYS["firstnames"]],
                            persondatadict[KEYS["hostess"]][KEYS["surname"]],
                            persondatadict[KEYS["hostess"]][KEYS["gender"]],
                            persondatadict[KEYS["hostess"]][KEYS["hostessBirthData"]][KEYS["birthDay"]],
                            persondatadict[KEYS["hostess"]][KEYS["hostessBirthData"]][KEYS["birthMonth"]],
                            persondatadict[KEYS["hostess"]][KEYS["hostessBirthData"]][KEYS["birthYear"]],
                            persondatadict[KEYS["approximatePage"]],
                            persondatadict[KEYS["manymarriages"]]



               ] }
        row["children"] = self._addChildren(persondatadict)
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
        return lrow

    def _writeToFile(self):
        self._writeCsvHeaders()
        for row in self.rowsofcsv:
            w = row["regular"] + row["children"]
            diff = self.childrenMax*3 - len(row["children"]) +3   #1 for childrencount column
            if diff > 0:            #tasaa rivit lisäämällä tyhjää
                w = w + [""]*diff #3 is the number of cells per child

            self.csvWriter.writerow(w)

    @abstractmethod
    def closeCsv(self):
        self._writeToFile()
        self.openedCsv.close()
        self.openedCsv = None
