from books.farmers.processData import ProcessData
from books.farmers.resultcsvbuilder import ResultCsvBuilder
from books.farmers.resultjsonbuilder import ResultJsonBuilder


class SmallFarmersExtractor:

    def __init__(self, update_callback):
        self._extractor = ProcessData(update_callback)
        self._results = None

    def process(self, xml_document):
        self._results = self._extractor.run_extraction(xml_document, '')

    def save_results(self, file, file_format='json'):
        if file_format == 'json':
            writer = ResultJsonBuilder()
            writer.openJson(file)

            for entry in self._results['entries']:
                try:
                    writer.writeEntry(entry["extractionResults"])
                except KeyError as e:
                    raise e

            writer.closeJson()
        elif file_format == 'csv':
            writer = ResultCsvBuilder()
            writer.openCsv(file)

            for entry in self._results['entries']:
                try:
                    writer.writeRow(entry["extractionResults"])
                except KeyError as e:
                    raise e


