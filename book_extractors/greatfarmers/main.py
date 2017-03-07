from book_extractors.processdata import ProcessData
from book_extractors.greatfarmers.resultcsvbuilder import ResultCsvBuilder
from book_extractors.greatfarmers.resultjsonbuilder import ResultJsonBuilder
from book_extractors.greatfarmers.extraction.extractionPipeline import ExtractionPipeline


class GreatFarmersExtractor:

    def __init__(self, update_callback):
        self._extractor_pipeline = ExtractionPipeline()
        self._extractor = ProcessData(self._extractor_pipeline, update_callback)
        self._results = None

    def process(self, person_data):
        self._results = self._extractor.run_extraction(person_data)

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


def get_great_farmers_data_entry(name, location, approximated_page, text):
    """
    Create extractor compatible dict from given parameters. Input to extractor should
    consist of dict of this form!
    :param name:
    :param location:
    :param approximated_page:
    :param text:
    :return:
    """
    return {
        'name': name,
        'location': location,
        'approximated_page': approximated_page,
        'text': text
    }

