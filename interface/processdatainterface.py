from abc import abstractmethod


class ProcessDataInterface:

    def __init__(self, callback):
        pass

    @abstractmethod
    def run_extraction(self, xml_document, file_path):
        """

        :param xml_document:
        :param file_path:
        :return:  {
            "errors": self.errorLogger.getErrors(),
            "entries": self.readDataEntries,
            "xmlDocument": self.xmlDataDocument,
            "file": filePath
            }
        """
        pass

    @abstractmethod
    def extract_one(self, xml_entry):
        """Can be used to extract only one entry after the main file"""
        pass

    def _process_all_entries(self):
        pass

    def _process_entry(self, entry):
        person_entry_dict = self.extractor.extraction(entry["xml"].text, entry, self.errorLogger)
        entry["extractionResults"] = person_entry_dict
        self.readDataEntries.append(entry)
        self.count +=1
        return entry

    def _create_entry(self, xmlEntry):
        return {"xml": xmlEntry, "extractionResults" : self._create_result_template()}

    def _create_result_template(self):
        pass

    def _handle_extraction_error_logging(self, exception, entry):
        pass

    def _finish_process(self):
        self._print_statistics()

    def _print_statistics(self):
        print ("Errors encountered: " + str(self.errors) + "/" + str(self.count))
        self.errorLogger.printErrorBreakdown()
