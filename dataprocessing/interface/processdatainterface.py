
from abc import abstractmethod
XMLPATH = "../xmldata/"
CSVPATH = "../csv/"

class ProcessDataInterface:


    def __init__(self, callback):
        pass

    #TODO: Nimeä uudestaan kuvaamaan että se palauttaa valmiin tuloksen?
    @abstractmethod
    def startExtractionProcess(self, filePath):
        """return {"errors": self.errorLogger.getErrors(), "entries": self.readDataEntries, "xmlDocument": self.xmlDataDocument,
                "file": filePath}"""
        pass

    @abstractmethod
    def extractOne(self, xmlEntry):
        """Can be used to extract only one entry after the main file"""
        #return entry
        pass

    #TODO: POISTA NÄMÄ SILLÄ SISÄINEN TOTEUTUS VOI OLLA MITÄ VAIN
    def _initProcess(self, filePath):
        pass

    def _processAllEntries(self):
        pass
        """
        i = 0
        ValueWrapper.reset_id_counter()
        for child in self.xmlDataDocument:
            entry = self._createEntry(child)
            ValueWrapper.xmlEntry = child
            try:
                self._processEntry(entry)
            except ExtractionException as e:
                self.readDataEntries.append(entry)
                self._handleExtractionErrorLogging(exception=e, entry=entry)

            i +=1
            ValueWrapper.reset_id_counter() #Resets the id-generator for each datafield of entry
            self.processUpdateCallbackFunction(i, self.xmlDataDocumentLen)
        """



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
        pass
        """return {"surname" : "", "firstnames" : "", "birthDay": "",
               "birthMonth" : "", "birthYear" : "", "birthLocation" : "",
               "profession" : "", "address" : "", "deathDay" : "",
               "deathMonth": "", "deathYear": "", "kaatunut": "",
               "deathLocation": "", "talvisota": "", "talvisotaregiments": "",
               "jatkosota": "", "jatkosotaregiments": "","rank": "",
               "kotiutusDay": "", "kotiutusMonth": "", "kotiutusYear": "",
               "kotiutusPlace": "", "medals": "","hobbies": "",
               "hasSpouse": "", "children": "", "childCount": ""}"""

    def _handleExtractionErrorLogging(self, exception, entry):
        pass

    def _finishProcess(self):
        self._printStatistics()


    def _printStatistics(self):
        print ("Errors encountered: " + str(self.errors) + "/" + str(self.count))
        self.errorLogger.printErrorBreakdown()


