from shared.exceptionlogger import ExceptionLogger
from book_extractors.karelians.extraction.extractionPipeline import ExtractionPipeline
from interface.processdatainterface import ProcessDataInterface
from book_extractors.karelians.extraction.extractionExceptions import ExtractionException


class ProcessData(ProcessDataInterface):

    def __init__(self, callback):
        self.extractor = None
        self.person_data = None
        self.read_data_entries = []
        self.processUpdateCallbackFunction = None
        self.processUpdateCallbackFunction = callback

    def run_extraction(self, person_input_data):
        self.person_data = person_input_data
        self._init_process()
        self._process_all_entries()
        return {"errors": self.errorLogger.getErrors(),
                "entries": self.read_data_entries
                }

    def _init_process(self):
        self.errors = 0
        self.count = 0
        self.errorLogger = ExceptionLogger()
        self.extractor = ExtractionPipeline(self.person_data)
        self.person_data_length = len(self.person_data)

    def _process_all_entries(self):
        i = 0

        for person in self.person_data:
            try:
                self.read_data_entries.append(self._process_entry(person))
            except ExtractionException as e:
                self.read_data_entries.append(person)
                self._handle_extraction_error_logging(exception=e, entry=person)

            i += 1
            self.processUpdateCallbackFunction(i, self.person_data_length)

    def _process_entry(self, person):
        person_results = self.extractor.process(person, self.errorLogger)
        person["extractionResults"] = person_results
        self.count += 1
        return person

    def extract_one(self, person_input_data):
        person_results = None
        try:
            person_results = self.extractor.process(person_input_data, self.errorLogger)
            person_results["extractionResults"] = person_results
        except ExtractionException as e:
            pass

        return person_results
