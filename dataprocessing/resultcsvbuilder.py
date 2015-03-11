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
        row = [persondatadict[KEYS["surname"]], persondatadict[KEYS["firstnames"]], persondatadict[KEYS["birthDay"]],
               persondatadict[KEYS["birthMonth"]], persondatadict[KEYS["birthYear"]], persondatadict[KEYS["birthLocation"]],
               persondatadict[KEYS["profession"]], persondatadict[KEYS["address"]], persondatadict[KEYS["deathDay"]],
               persondatadict[KEYS["deathMonth"]], persondatadict[KEYS["deathYear"]], persondatadict[KEYS["kaatunut"]],
               persondatadict[KEYS["deathLocation"]], persondatadict[KEYS["talvisota"]], persondatadict[KEYS["talvisotaregiments"]],
               persondatadict[KEYS["jatkosota"]], persondatadict[KEYS["jatkosotaregiments"]],persondatadict[KEYS["rank"]],
               persondatadict[KEYS["kotiutusDay"]], persondatadict[KEYS["kotiutusMonth"]], persondatadict[KEYS["kotiutusYear"]],
               persondatadict[KEYS["kotiutusPlace"]], persondatadict[KEYS["medals"]],persondatadict[KEYS["hobbies"]],
               persondatadict[KEYS["hasSpouse"]]]

        row = self._addOtherChildrenCells(row=row, persondatadict=persondatadict)
        row = self._addSpouseDataToRow(row=row, persondatadict=persondatadict)
        return row

    def _addOtherChildrenCells(self, row, persondatadict):
        if "children" in persondatadict:
            row += [persondatadict["children"], persondatadict["childCount"]]
        else:
            row += ["", ""]
        return row

    def _addSpouseDataToRow(self,row, persondatadict):
        if persondatadict[KEYS["spouseCount"]] > 0:
            for wife in persondatadict[KEYS["wifeList"]]:
                wifeRow = self._createWifeRowFromDict(wife)
                row += wifeRow
        return row

    def _createWifeRowFromDict(self, wife):
        wifeRow =   [wife[KEYS["weddingYear"]], wife[KEYS["spouseName"]], wife[KEYS["spouseBirthData"]][KEYS["birthDay"]],
                     wife[KEYS["spouseBirthData"]][KEYS["birthMonth"]], wife[KEYS["spouseBirthData"]][KEYS["birthYear"]],
                     wife[KEYS["spouseBirthLocation"]],  wife[KEYS["spouseDeathData"]][KEYS["deathDay"]],
                     wife[KEYS["spouseDeathData"]][KEYS["deathMonth"]], wife[KEYS["spouseDeathData"]][KEYS["deathYear"]],
                     wife[KEYS["spouseDeathData"]][KEYS["deathLocation"]], wife[KEYS["children"]][KEYS["childCount"]],
                     wife[KEYS["children"]][KEYS["separated"]][KEYS["miehEd"]], wife[KEYS["children"]][KEYS["separated"]][KEYS["nyk"]],
                     wife[KEYS["children"]][KEYS["separated"]][KEYS["psoEd"]]]
        return wifeRow

    def closeCsv(self):
        self.openedCsv.close()
        self.openedCsv = None