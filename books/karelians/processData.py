from shared.exceptionlogger import ExceptionLogger
from books.karelians.extraction.extractionPipeline import ExtractionPipeline
from interface.processdatainterface import ProcessDataInterface
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import ExtractionException


class ProcessData(ProcessDataInterface):

    def __init__(self, callback):
        self.dataFilename = ""
        self.csvBuilder = None
        self.extractor = None
        self.xmlDataDocument = None
        self.readDataEntries = []
        self.processUpdateCallbackFunction = None
        self.processUpdateCallbackFunction = callback

    def startExtractionProcess(self, xmlDocument, file_path):
        self.xmlDataDocument = xmlDocument
        self.dataFilename = file_path
        self._initProcess()
        self._processAllEntries()
        return {"errors": self.errorLogger.getErrors(), "entries": self.readDataEntries, "xmlDocument": self.xmlDataDocument,
                "file": file_path}

    def _initProcess(self):
        self.errors = 0
        self.count = 0
        self.errorLogger = ExceptionLogger()


        self.extractor = ExtractionPipeline(self.xmlDataDocument)
        self.xmlDataDocumentLen = len(self.xmlDataDocument)

    def _processAllEntries(self):
        ValueWrapper.reset_id_counter()
        i = 0

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

    def _processEntry(self, entry):
        personEntryDict = self.extractor.process(entry["xml"].text, entry, self.errorLogger)
        entry["extractionResults"] = personEntryDict
        self.readDataEntries.append(entry)
        self.count +=1
        return entry

    def _createEntry(self, xmlEntry):
        return {"xml": xmlEntry, "extractionResults" : self._createResultTemplate()}

    def extractOne(self, xmlEntry):
        ValueWrapper.reset_id_counter()
        entry = self._createEntry(xmlEntry)
        ValueWrapper.xmlEntry = xmlEntry
        try:
            personEntryDict = self.extractor.process(entry["xml"].text, entry, self.errorLogger)
            entry["extractionResults"] = personEntryDict
        except ExtractionException as e:
            pass

        return entry
