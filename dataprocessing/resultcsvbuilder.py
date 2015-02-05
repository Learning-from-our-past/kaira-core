# -*- coding: utf-8 -*-
import ntpath
import unicodecsv

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
        self.initCsv()


    def initCsv(self):
        self.openedCsv = open(self.CSVPATH + self.filename+ ".csv", "wb")
        self.csvWriter = unicodecsv.writer(self.openedCsv, delimiter="&")
        self.writeCsvHeaders()

    def writeCsvHeaders(self):
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
        row = self.createRowFromDict(dataDict)
        self.csvWriter.writerow(row)

    #tranforms the dict of the entry to a format which can be written into csv
    def createRowFromDict(self, persondatadict):
        row = [persondatadict["surname"], persondatadict["firstnames"], persondatadict["birthDay"],
               persondatadict["birthMonth"], persondatadict["birthYear"], persondatadict["birthLocation"],
               persondatadict["profession"], persondatadict["address"], persondatadict["deathDay"],
               persondatadict["deathMonth"], persondatadict["deathYear"], persondatadict["kaatunut"],
               persondatadict["deathLocation"], persondatadict["talvisota"], persondatadict["talvisotaregiments"],
               persondatadict["jatkosota"], persondatadict["jatkosotaregiments"],persondatadict["rank"],
               persondatadict["kotiutusDay"], persondatadict["kotiutusMonth"], persondatadict["kotiutusYear"],
               persondatadict["kotiutusPlace"], persondatadict["medals"],persondatadict["hobbies"],
               persondatadict["hasSpouse"]]

        if "children" in persondatadict:
            #other children
            row += [persondatadict["children"], persondatadict["childCount"]]
        else:
            row += ["", ""]

        #list all spouses data:
        if persondatadict["spouseCount"] > 0:
            for wife in persondatadict["wifeList"]:
                wifeRow = [wife["weddingYear"], wife["spouseName"], wife["spouseBirthData"]["birthDay"],
                           wife["spouseBirthData"]["birthMonth"], wife["spouseBirthData"]["birthYear"],
                                     wife["spouseBirthLocation"],  wife["spouseDeathData"]["deathDay"],
                                     wife["spouseDeathData"]["deathMonth"], wife["spouseDeathData"]["deathYear"],
                                     wife["spouseDeathData"]["deathLocation"], wife["children"]["childCount"],
                                     wife["children"]["separated"]["miehEd"], wife["children"]["separated"]["nyk"],
                                     wife["children"]["separated"]["psoEd"]]
                row += wifeRow

        #add other children which don't have wife associated into them
        return row

    def closeCsv(self):
        self.openedCsv.close()
        self.openedCsv = None