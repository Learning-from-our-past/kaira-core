# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
from extractionExceptions import *
from dataExtraction import DataExtraction
from extractionExceptions import *
from chunkerCheck import ChunkChecker
import guitool.combineTool as CombineTool
import guitool.groupSelection as GUITool
from lxml import etree



def startProcess(filePath, callback):
    #This script runs the exctraction process by using DataExtraction class's services.
    errors = 0
    count = 0
    file = filePath #"rintamamiehet11_tags"
    root = readData.getXMLroot(file + ".xml")
    extractor = DataExtraction()
    chunkerCheck = ChunkChecker()


    errorNodes = []

    #tranforms the dict of the entry to a format which can be written into csv
    def createRow(d):
        row = [d["surname"], d["firstnames"], d["birthDay"], d["birthMonth"], d["birthYear"], d["birthLocation"], d["profession"], d["address"], d["deathDay"], d["deathMonth"], d["deathYear"], d["kaatunut"], d["deathLocation"], d["talvisota"], d["talvisotaregiments"], d["jatkosota"], d["jatkosotaregiments"], d["rank"], d["kotiutusDay"], d["kotiutusMonth"], d["kotiutusYear"], d["kotiutusPlace"], d["medals"], d["hobbies"], d["hasSpouse"]]
        """
        """
        if "children" in d:
            row += [d["children"], d["childCount"]]
        else:
            row += ["", ""]
        #list all spouses data:
        if d["spouseCount"] > 0:
            for wife in d["wifeList"]:
                wifeRow = [wife["weddingYear"], wife["spouseName"], wife["spouseBirthData"]["birthDay"], wife["spouseBirthData"]["birthMonth"], wife["spouseBirthData"]["birthYear"],
                                     wife["spouseBirthLocation"],  wife["spouseDeathData"]["deathDay"], wife["spouseDeathData"]["deathMonth"], wife["spouseDeathData"]["deathYear"],
                                     wife["spouseDeathData"]["deathLocation"], wife["children"]["childCount"], wife["children"]["children"]]
                row += wifeRow

        #add other children which don't have wife associated into them

        return row

    #saves information about the error entry so that it can be fixed.
    class ExceptionLogger:
        errorsListing = {}
        def logError(self, exceptionType, entry):

            if exceptionType in self.errorsListing:
                self.errorsListing[exceptionType].append({"child": entry})
            else:
                self.errorsListing[exceptionType] = [{"child": entry}]

        def printErrorBreakdown(self):
            print "ERROR breakdown: "
            for key, value in self.errorsListing.iteritems():
                print key
                print len(value)

        def getErrors(self):
            return self.errorsListing




    #save the extract4ed info to a csv file:
    with open(file +".csv", "wb") as results:
        with open(file +"_errors.csv", "wb") as errorcsv:
            writer = unicodecsv.writer(results, delimiter="&")
            writer.writerow(["surname", "first names", "birthDay", "birthMonth", "birthYear", "birthLocation", "Profession", "InterviewAddress", "deathDay", "deathMonth", "deathYear", "fallen", "deathLocation", "Served in Talvisota", "Talvisota regiments", "Served in Jatkosota", "Jatkosota regiments","Rank", "DemobilizationDay", "DemobilizationMonth", "DemobilizationYear", "DemobilizationPlace", "Medals", "Hobbies", "hasSpouse", "otherChildren", "otherChildrenCount", "weddingYear",
                             "spouseName", "spouseBirthDay", "spouseBirthMonth","spouseBirthYear","spouseBirthLocation", "spouseDeathDay", "spouseDeathMonth","spouseDeathYear", "spouseDeathLocation", "childCount", "children",
                             "weddingYear2",
                             "spouseName2", "spouseBirthDay2", "spouseBirthMonth2","spouseBirthYear2","spouseBirthLocation2", "spouseDeathDay2", "spouseDeathMonth2","spouseDeathYear2", "spouseDeathLocation2", "childCount2", "children2"
                             ])

            ewriter = unicodecsv.writer(errorcsv, delimiter=";")
            ewriter.writerow(["Exception","Details", "type", "Entry text"])
            errorLogger = ExceptionLogger()

            for child in root:
                try:
                    d = extractor.extraction(child.text, child, errorLogger)
                    chunkerCheck.checkEntry(child, child.sourceline)
                    writer.writerow(createRow(d))
                    count +=1
                except ExtractionException as e:

                    errorLogger.logError(e.eType, child)
                    #errorNodes.append({"child": child})
                    ewriter.writerow([e.message, e.details, e.eType, child.text])
                    errors +=1
                    count +=1
                continue


    print "Errors encountered: " + str(errors) + "/" + str(count)

    for item in chunkerCheck.getSuspiciousEntries():
        errorLogger.logError("SUSPICIOUSCHUNK", item["child"])

    errorLogger.printErrorBreakdown()

    #callback()
    return {"errors": errorLogger.getErrors(), "root" : root, "file": file}





def saveModificationsToFile(file, root):
    #write modifications to a new xml-file:
    print "Kirjoitetaan " + file
    f = open(file + ".xml", 'w')
    f.write(etree.tostring(root, pretty_print=True, encoding='unicode').encode("utf8"))
    f.close()
    print "valmis"

if __name__ == '__main__':
    startProcess("rintamamiehet11_tags")