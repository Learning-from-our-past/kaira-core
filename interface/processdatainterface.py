from abc import abstractmethod


class ProcessDataInterface:

    def __init__(self, callback):
        pass

    @abstractmethod
    def run_extraction(self, xml_document, file_path):
        pass

    @abstractmethod
    def extract_one(self, xml_entry):
        """Can be used to extract only one entry after the main file"""
        pass

    def _process_all_entries(self):
        pass

    def _handle_extraction_error_logging(self, exception, entry):
        pass

    def _finish_process(self):
        self._print_statistics()

    def _print_statistics(self):
        print ("Errors encountered: " + str(self.errors) + "/" + str(self.count))
        self.errorLogger.printErrorBreakdown()
