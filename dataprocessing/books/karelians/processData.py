from shared.exceptionlogger import ExceptionLogger
from books.karelians.extraction.extractionPipeline import ExtractionPipeline
from interface.processdatainterface import ProcessDataInterface
from lxml import etree
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

    def startExtractionProcess(self, file_path):
        self._initProcess(file_path)
        self._processAllEntries()
        #self._finishProcess()
        #self.processUpdateCallbackFunction(self.xmlDataDocumentLen, self.xmlDataDocumentLen)    #DUMMY
        return {"errors": self.errorLogger.getErrors(), "entries": self.readDataEntries, "xmlDocument": self.xmlDataDocument,
                "file": file_path}

    def _initProcess(self, file_path):
        self.errors = 0
        self.count = 0
        self.errorLogger = ExceptionLogger()
        self.dataFilename = file_path
        self.xmlDataDocument = self._getXMLroot(file_path)

        self.extractor = ExtractionPipeline(self.xmlDataDocument)
        self.xmlDataDocumentLen = len(self.xmlDataDocument)
        print ("XML file elements: " + str(len(self.xmlDataDocument)))

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
        pass


    def _getXMLroot(self, filepath):
        #read the data in XML-format to be processed
        tree = etree.parse(filepath) #ET.parse(filepath)
        return tree.getroot()