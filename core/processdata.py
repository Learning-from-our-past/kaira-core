class ProcessData:
    def __init__(self, extraction_pipeline, extraction_result_map, callback=None):
        self.extraction_pipeline = extraction_pipeline
        self._extraction_result_map = extraction_result_map
        self._person_data_stream = None
        self.read_data_entries = []
        self.processUpdateCallbackFunction = callback

    def run_extraction(self, person_input_stream):
        self._person_data_stream = person_input_stream
        self._init_process()
        self._process_all_entries()
        return {"entries": self.read_data_entries}

    def _init_process(self):
        self.errors = 0
        self.count = 0

    def _process_all_entries(self):
        i = 0

        for person in self._person_data_stream.read_entry_from_xml():
            try:
                self.read_data_entries.append(self._process_entry(person))
            except ExtractionException as e:
                self.read_data_entries.append(person)

            i += 1

            if self.processUpdateCallbackFunction:
                self.processUpdateCallbackFunction(i)

    def _process_entry(self, person):
        person_results = self.extraction_pipeline.process(person)
        person["extractionResults"] = person_results
        self.count += 1
        # Clear the storage for extractor results used in dependency resolving
        self._extraction_result_map.clear()
        return person


class ExtractionException(Exception):
    message = u""
    details = u""
    eType = "OTHER"

    def __init__(self):
        pass

    def __unicode__(self):
        return self.message
