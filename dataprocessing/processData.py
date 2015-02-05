# -*- coding: utf-8 -*-
import readData

import ntpath
import unicodecsv
from dataExtraction import DataExtraction
from extractionExceptions import *
from chunkerCheck import ChunkChecker
from lxml import etree
from exceptionlogger import ExceptionLogger
from resultcsvbuilder import ResultCsvBuilder

XMLPATH = "../xmldata/"
CSVPATH = "../csv/"

class ProcessData:
    dataFilename = ""
    csvBuilder = None
    extractor = None
    chunkerCheck = None

    def startProcess(self, filePath, callback):

        #TODO: INIT FUNCTION
        #This script runs the exctraction process by using DataExtraction class's services.
        errors = 0
        count = 0
        file = filePath
        self.csvBuilder = ResultCsvBuilder()
        self.csvBuilder.openCsv(filePath)
        self.extractor = DataExtraction()
        self.chunkerCheck = ChunkChecker()
        self.errorLogger = ExceptionLogger()

        root = readData.getXMLroot(file + ".xml")
        print "XML file elements: " + str(len(root))

        #TODO: FUNCTION FOR EXTRACT LOOP
        #TODO: Error writer to own class and functions
        #save the extracted info to a csv file:
        with open(file +"_errors.csv", "wb") as errorcsv:
            ewriter = unicodecsv.writer(errorcsv, delimiter=";")
            ewriter.writerow(["Exception","Details", "type", "Entry text"])

            for child in root:
                try:
                    personEntryDict = self.extractor.extraction(child.text, child, self.errorLogger)
                    self.chunkerCheck.checkEntry(child, child.sourceline)
                    self.csvBuilder.writeRow(personEntryDict)
                    count +=1
                except ExtractionException as e:
                    self.errorLogger.logError(e.eType, child)
                    ewriter.writerow([e.message, e.details, e.eType, child.text])
                    errors +=1
                    count +=1
                continue


        print "Errors encountered: " + str(errors) + "/" + str(count)

        #TODO: FUNCTION OR REMOVE
        for item in self.chunkerCheck.getSuspiciousEntries():
            self.errorLogger.logError("SUSPICIOUSCHUNK", item["child"])

        self.errorLogger.printErrorBreakdown()

        self.csvBuilder
        #callback()
        return {"errors": self.errorLogger.getErrors(), "root" : root, "file": file}





    def saveModificationsToFile(self, file, root):
        #write modifications to a new xml-file:
        print "Kirjoitetaan " + file
        f = open(XMLPATH + self.dataFilename + ".xml", 'w')
        f.write(etree.tostring(root, pretty_print=True, encoding='unicode').encode("utf8"))
        f.close()
        print "valmis"

