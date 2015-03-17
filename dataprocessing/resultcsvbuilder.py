# -*- coding: utf-8 -*-
import ntpath
import csv
from extractionkeys import KEYS
class ResultCsvBuilder:
    CSVPATH = "../csv/"
    filepath = ""
    filename = ""
    openedCsv = None
    csvWriter = None

    def __init__(self):
        pass

    def openCsv(self, filepath):
        self.filepath = filepath
        self.filename = ntpath.basename(self.filepath)
        self._initCsv()


    def _initCsv(self):
        self.openedCsv = open(self.CSVPATH + self.filename[:-4]+ ".csv", "w", newline='', encoding="utf-8")
        self.csvWriter = csv.writer(self.openedCsv, delimiter="&")
        self._writeCsvHeaders()

    def _writeCsvHeaders(self):
         self.csvWriter.writerow(["surname", "first names", "birthDay", "birthMonth", "birthYear", "birthLocation",
                                  "Profession", "InterviewAddress", "deathDay", "deathMonth", "deathYear", "fallen",
                                  "deathLocation", "Served in Talvisota", "Talvisota regiments", "Served in Jatkosota",
                                  "Jatkosota regiments","Rank", "DemobilizationDay", "DemobilizationMonth",
                                  "DemobilizationYear", "DemobilizationPlace", "Medals", "Hobbies", "hasSpouse",
                                  "otherChildren", "otherChildrenCount", "weddingYear","spouseName", "spouseBirthDay",
                                  "spouseBirthMonth","spouseBirthYear","spouseBirthLocation", "spouseDeathDay",
                                  "spouseDeathMonth","spouseDeathYear", "spouseDeathLocation", "childCount",
                                  "Man's previous marriage", "Current marriage", "Spouse's previous marriage",
                                  "weddingYear2","spouseName2", "spouseBirthDay2", "spouseBirthMonth2","spouseBirthYear2",
                                  "spouseBirthLocation2", "spouseDeathDay2", "spouseDeathMonth2","spouseDeathYear2",
                                  "spouseDeathLocation2", "childCount2", "Man's previous marriage2", "Current marriage2",
                                  "Spouse's previous marriage2"
                                 ])

    def writeRow(self, dataDict):
        row = self._createRowFromDict(dataDict)
        self.csvWriter.writerow(row)

    #tranforms the dict of the entry to a format which can be written into csv
    def _createRowFromDict(self, persondatadict):
        row = [persondatadict[KEYS["surname"]].value, persondatadict[KEYS["firstnames"]].value, persondatadict[KEYS["birthDay"]].value,
               persondatadict[KEYS["birthMonth"]].value, persondatadict[KEYS["birthYear"]].value, persondatadict[KEYS["birthLocation"]].value,
               persondatadict[KEYS["profession"]].value, persondatadict[KEYS["address"]].value, persondatadict[KEYS["deathDay"]].value,
               persondatadict[KEYS["deathMonth"]].value, persondatadict[KEYS["deathYear"]].value, persondatadict[KEYS["kaatunut"]].value,
               persondatadict[KEYS["deathLocation"]].value, persondatadict[KEYS["talvisota"]].value, persondatadict[KEYS["talvisotaregiments"]].value,
               persondatadict[KEYS["jatkosota"]].value, persondatadict[KEYS["jatkosotaregiments"]].value,persondatadict[KEYS["rank"]].value,
               persondatadict[KEYS["kotiutusDay"]].value, persondatadict[KEYS["kotiutusMonth"]].value, persondatadict[KEYS["kotiutusYear"]].value,
               persondatadict[KEYS["kotiutusPlace"]].value, persondatadict[KEYS["medals"]].value,persondatadict[KEYS["hobbies"]].value,
               persondatadict[KEYS["hasSpouse"]].value]

        row = self._addOtherChildrenCells(row=row, persondatadict=persondatadict)
        row = self._addSpouseDataToRow(row=row, persondatadict=persondatadict)
        return row

    def _addOtherChildrenCells(self, row, persondatadict):
        if "children" in persondatadict:
            row += [persondatadict["children"], persondatadict["childCount"]].value
        else:
            row += ["", ""]
        return row

    def _addSpouseDataToRow(self,row, persondatadict):
        if persondatadict[KEYS["spouseCount"]].value > 0:
            for wife in persondatadict[KEYS["wifeList"]].value:
                wifeRow = self._createWifeRowFromDict(wife.value)
                row += wifeRow
        return row

    def _createWifeRowFromDict(self, wife):
        wifeRow =   [wife[KEYS["weddingYear"]].value, wife[KEYS["spouseName"]].value, wife[KEYS["spouseBirthData"]].value[KEYS["birthDay"]].value,
                     wife[KEYS["spouseBirthData"]].value[KEYS["birthMonth"]].value, wife[KEYS["spouseBirthData"]].value[KEYS["birthYear"]].value,
                     wife[KEYS["spouseBirthLocation"]].value,  wife[KEYS["spouseDeathData"]].value[KEYS["deathDay"]].value,
                     wife[KEYS["spouseDeathData"]].value[KEYS["deathMonth"]].value, wife[KEYS["spouseDeathData"]].value[KEYS["deathYear"]].value,
                     wife[KEYS["spouseDeathData"]].value[KEYS["deathLocation"]].value, wife[KEYS["children"]].value[KEYS["childCount"]].value,
                     wife[KEYS["children"]].value[KEYS["separated"]].value[KEYS["miehEd"]].value, wife[KEYS["children"]].value[KEYS["separated"]].value[KEYS["nyk"]].value,
                     wife[KEYS["children"]].value[KEYS["separated"]].value[KEYS["psoEd"]].value]
        return wifeRow

    def closeCsv(self):
        self.openedCsv.close()
        self.openedCsv = None