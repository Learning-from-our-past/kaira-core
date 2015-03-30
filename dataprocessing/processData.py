# -*- coding: utf-8 -*-
from lxml import etree

import readData
from extraction.dataExtraction import DataExtraction
from extraction.extractionExceptions import *
from exceptionlogger import ExceptionLogger
from resultcsvbuilder import ResultCsvBuilder
from errorcsvbuilder import ErrorCsvBuilder
from extractionkeys import ValueWrapper

XMLPATH = "../xmldata/"
CSVPATH = "../csv/"



class ProcessData:

    def __init__(self, callback):
        self.dataFilename = ""
        self.csvBuilder = None
        self.errorCsvBuilder = None
        self.extractor = None
        self.chunkerCheck = None
        self.errors = 0
        self.count = 0
        self.xmlDataDocument = None
        self.readDataEntries = []
        self.processUpdateCallbackFunction = None
        self.processUpdateCallbackFunction = callback

    #TODO: Nimeä uudestaan kuvaamaan että se palauttaa valmiin tuloksen?
    def startExtractionProcess(self, filePath):
        self._initProcess(filePath)
        self._processAllEntries()
        self._finishProcess()
        return {"errors": self.errorLogger.getErrors(), "entries": self.readDataEntries, "xmlDocument": self.xmlDataDocument,
                "file": filePath}


    def extractOne(self, xmlEntry):
        """Can be used to extract only one entry after the main file"""
        entry = self._createEntry(xmlEntry)
        ValueWrapper.xmlEntry = xmlEntry
        try:
            personEntryDict = self.extractor.extraction(entry["xml"].text, entry, self.errorLogger)
            entry["extractionResults"] = personEntryDict
        except ExtractionException as e:
            pass

        return entry

    def _initProcess(self, filePath):
        self.errors = 0
        self.count = 0
        #self.csvBuilder = ResultCsvBuilder()
        #self.csvBuilder.openCsv(filePath)
        self.errorCsvBuilder = ErrorCsvBuilder()
        self.errorCsvBuilder.openCsv(filePath)
        self.errorLogger = ExceptionLogger()
        self.dataFilename = filePath
        self.xmlDataDocument = readData.getXMLroot(filePath)

        self.extractor = DataExtraction(self.xmlDataDocument)
        self.xmlDataDocumentLen = len(self.xmlDataDocument)
        print ("XML file elements: " + str(len(self.xmlDataDocument)))

    def _processAllEntries(self):
        i = 0
        for child in self.xmlDataDocument:
            entry = self._createEntry(child)
            ValueWrapper.xmlEntry = child
            try:
                self._processEntry(entry)
            except ExtractionException as e:
                self.readDataEntries.append(entry)    #TODO: Probably better idea to pass dict with keys with empty fields?
                self._handleExtractionErrorLogging(exception=e, entry=entry)

            i +=1
            ValueWrapper.reset_id_counter() #Resets the id-generator for each datafield of entry
            self.processUpdateCallbackFunction(i, self.xmlDataDocumentLen)



    def _processEntry(self, entry):
        personEntryDict = self.extractor.extraction(entry["xml"].text, entry, self.errorLogger)
        entry["extractionResults"] = personEntryDict
        self.readDataEntries.append(entry)
        #self.csvBuilder.writeRow(personEntryDict)
        self.count +=1
        return entry

    def _createEntry(self, xmlEntry):
        return {"xml": xmlEntry, "extractionResults" : self._createResultTemplate()}

    def _createResultTemplate(self):
        return {"surname" : "", "firstnames" : "", "birthDay": "",
               "birthMonth" : "", "birthYear" : "", "birthLocation" : "",
               "profession" : "", "address" : "", "deathDay" : "",
               "deathMonth": "", "deathYear": "", "kaatunut": "",
               "deathLocation": "", "talvisota": "", "talvisotaregiments": "",
               "jatkosota": "", "jatkosotaregiments": "","rank": "",
               "kotiutusDay": "", "kotiutusMonth": "", "kotiutusYear": "",
               "kotiutusPlace": "", "medals": "","hobbies": "",
               "hasSpouse": "", "children": "", "childCount": ""}

    def _handleExtractionErrorLogging(self, exception, entry):
        self.errorLogger.logError(exception.eType, entry)
        self.errorCsvBuilder.writeRow([exception.message, exception.details, exception.eType, entry["xml"].text])
        self.errors +=1
        self.count +=1

    def _finishProcess(self):
        self._printStatistics()
        #self.csvBuilder.closeCsv()
        self.errorCsvBuilder.closeCsv()

    def _printStatistics(self):
        print ("Errors encountered: " + str(self.errors) + "/" + str(self.count))
        self.errorLogger.printErrorBreakdown()

    #TODO: Muu paikka?
    def saveModificationsToFile(self):
        #write modifications to a new xml-file:
        print ("Kirjoitetaan ")
        f = open(self.dataFilename + ".xml", 'w')
        f.write(etree.tostring(self.xmlDataDocument, pretty_print=True, encoding='unicode').encode("utf8"))
        f.close()
        print ("valmis")

