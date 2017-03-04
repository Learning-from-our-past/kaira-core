from books.karelians.chunktextfile import PersonPreprocessor as KarelianChunk
from books.karelians.processData import ProcessData
from books.karelians.resultcsvbuilder import ResultCsvBuilder
from books.karelians.resultjsonbuilder import ResultJsonBuilder
import os


class KarelianExtractor:

    def __init__(self, update_callback):
        self._extractor = ProcessData(update_callback)
        self._results = None

    def process(self, xml_document):
        self._results = self._extractor.startExtractionProcess(xml_document, '')

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


