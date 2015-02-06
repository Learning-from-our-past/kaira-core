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
from errorcsvbuilder import ErrorCsvBuilder

XMLPATH = "../xmldata/"
CSVPATH = "../csv/"

class ProcessData:
    dataFilename = ""
    csvBuilder = None
    errorCsvBuilder = None
    extractor = None
    chunkerCheck = None
    errors = 0
    count = 0
    xmlDataDocument = None

    #TODO: Nimeä uudestaan kuvaamaan että se palauttaa valmiin tuloksen?
    def startExtractionProcess(self, filePath):
        self._initProcess(filePath)
        self._processAllEntries()
        self._finishProcess()
        return {"errors": self.errorLogger.getErrors(), "xmlDataDocument" : self.xmlDataDocument, "file": file}

    def _initProcess(self, filePath):
        self.errors = 0
        self.count = 0
        self.csvBuilder = ResultCsvBuilder()
        self.csvBuilder.openCsv(filePath)
        self.errorCsvBuilder = ErrorCsvBuilder()
        self.errorCsvBuilder.openCsv(filePath)
        self.extractor = DataExtraction()
        self.chunkerCheck = ChunkChecker()
        self.errorLogger = ExceptionLogger()
        self.xmlDataDocument = readData.getXMLroot(filePath + ".xml")
        print "XML file elements: " + str(len(self.xmlDataDocument))

    def _processAllEntries(self):
        for child in self.xmlDataDocument:
            try:
                self._processEntry(child)
            except ExtractionException as e:
                self._handleExtractionErrorLogging(exception=e, entry=child)

    def _processEntry(self, entry):
        personEntryDict = self.extractor.extraction(entry.text, entry, self.errorLogger)
        self.csvBuilder.writeRow(personEntryDict)
        self.count +=1

    def _handleExtractionErrorLogging(self, exception, entry):
        self.errorLogger.logError(exception.eType, entry)
        self.errorCsvBuilder.writeRow([exception.message, exception.details, exception.eType, entry.text])
        self.errors +=1
        self.count +=1

    def _finishProcess(self):
        self._printStatistics()
        self.csvBuilder.closeCsv()
        self.errorCsvBuilder.closeCsv()

    def _printStatistics(self):
        print "Errors encountered: " + str(self.errors) + "/" + str(self.count)
        self.errorLogger.printErrorBreakdown()

    #TODO: Muu paikka?
    def saveModificationsToFile(self, file, root):
        #write modifications to a new xml-file:
        print "Kirjoitetaan " + file
        f = open(XMLPATH + self.dataFilename + ".xml", 'w')
        f.write(etree.tostring(root, pretty_print=True, encoding='unicode').encode("utf8"))
        f.close()
        print "valmis"

