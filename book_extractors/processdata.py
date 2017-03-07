from shared.exceptionlogger import ExceptionLogger
from book_extractors.extraction_exceptions import ExtractionException


class ProcessData:

    def __init__(self, extraction_pipeline, callback):
        self.extraction_pipeline = extraction_pipeline
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
        self.person_data_length = len(self.person_data)

    def _process_all_entries(self):
        i = 0

        for person in self.person_data:
            try:
                self.read_data_entries.append(self._process_entry(person))
            except ExtractionException as e:
                self.read_data_entries.append(person)

            i += 1
            self.processUpdateCallbackFunction(i, self.person_data_length)

    def _process_entry(self, person):
        person_results = self.extraction_pipeline.process(person, self.errorLogger)
        person["extractionResults"] = person_results
        self.count += 1
        return person

    def extract_one(self, person_input_data):
        person_results = self.extraction_pipeline.process(person_input_data, self.errorLogger)
        person_results["extractionResults"] = person_results

        return person_results
