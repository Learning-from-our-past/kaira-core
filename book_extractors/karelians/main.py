from book_extractors.karelians.processData import ProcessData
from book_extractors.karelians.resultcsvbuilder import ResultCsvBuilder
from book_extractors.karelians.resultjsonbuilder import ResultJsonBuilder


class KarelianExtractor:

    def __init__(self, update_callback):
        self._extractor = ProcessData(update_callback)
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


def get_karelian_data_entry(name, approximated_page, text, img_path=''):
    """
    Create extractor compatible dict from given parameters. Input to extractor should
    consist of dict of this form!
    :param name:
    :param approximated_page:
    :param text:
    :return:
    """
    return {
        'name': name,
        'approximated_page': approximated_page,
        'image_path': img_path,
        'text': text
    }
