from shared.exceptionlogger import ExceptionLogger
from books.farmers.extraction.extractionPipeline import ExtractionPipeline
from interface.processdatainterface import ProcessDataInterface
from lxml import etree
from interface.valuewrapper import ValueWrapper
from books.farmers.extraction.extractionExceptions import ExtractionException
class ProcessData(ProcessDataInterface):


    def __init__(self, callback):
        self.dataFilename = ""
        self.csvBuilder = None
        self.extractor = None
        self.xmlDataDocument = None
        self.readDataEntries = []
        self.processUpdateCallbackFunction = None
        self.processUpdateCallbackFunction = callback

    def run_extraction(self, xml_document, file_path):
        self.xmlDataDocument = xml_document
        self.dataFilename = file_path
        self._initProcess()
        self._process_all_entries()
        #self._finishProcess()
        #self.processUpdateCallbackFunction(self.xmlDataDocumentLen, self.xmlDataDocumentLen)    #DUMMY
        return {"errors": self.errorLogger.getErrors(), "entries": self.readDataEntries, "xmlDocument": self.xmlDataDocument,
                "file": file_path}

    def _initProcess(self):
        self.errors = 0
        self.count = 0
        self.errorLogger = ExceptionLogger()


        self.extractor = ExtractionPipeline(self.xmlDataDocument)
        self.xmlDataDocumentLen = len(self.xmlDataDocument)

    def _process_all_entries(self):
        ValueWrapper.reset_id_counter()
        i = 0

        for child in self.xmlDataDocument:
            entry = self._create_entry(child)
            ValueWrapper.xmlEntry = child
            try:
                self._process_entry(entry)
            except ExtractionException as e:
                self.readDataEntries.append(entry)
                self._handle_extraction_error_logging(exception=e, entry=entry)

            i +=1
            ValueWrapper.reset_id_counter() #Resets the id-generator for each datafield of entry
            self.processUpdateCallbackFunction(i, self.xmlDataDocumentLen)

    def _process_entry(self, entry):
        personEntryDict = self.extractor.process(entry["xml"].text, entry, self.errorLogger)
        entry["extractionResults"] = personEntryDict
        self.readDataEntries.append(entry)
        self.count +=1
        return entry


    def _create_entry(self, xmlEntry):
        return {"xml": xmlEntry, "extractionResults" : self._create_result_template()}

    def extract_one(self, xml_entry):
        ValueWrapper.reset_id_counter()
        entry = self._create_entry(xml_entry)
        ValueWrapper.xmlEntry = xml_entry
        try:
            personEntryDict = self.extractor.process(entry["xml"].text, entry, self.errorLogger)
            entry["extractionResults"] = personEntryDict
        except ExtractionException as e:
            pass
        return entry
