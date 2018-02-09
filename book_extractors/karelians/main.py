from book_extractors.processdata import ProcessData
from book_extractors.karelians.resultjsonbuilder import ResultJsonBuilder
from shared.gender_extract import Gender
from pipeline_creation.yaml_parser import YamlParser
from pipeline_creation.dependency_resolver import ExtractorResultsMap

BOOK_SERIES_ID = 'siirtokarjalaiset'    # Used to identify this book series in xml files


class KarelianBooksExtractor:

    def __init__(self, update_callback):
        Gender.load_names()
        self._extraction_result_map = ExtractorResultsMap()
        self._parser = YamlParser(self._extraction_result_map)
        self._extractor_pipeline = self._parser.build_pipeline_from_yaml('./book_extractors/karelians/config.yaml')
        self._extractor = ProcessData(self._extractor_pipeline, self._extraction_result_map, update_callback)
        self._results = None

    def process(self, person_data):
        self._results = self._extractor.run_extraction(person_data)

    def save_results(self, file, file_format='json'):
        if file_format == 'json':
            writer = ResultJsonBuilder()
            writer.openJson(file)

            for entry in self._results['entries']:
                try:
                    writer.writeEntry(entry["extractionResults"][0])    # Leave metadata objects out
                except KeyError as e:
                    raise e

            writer.closeJson()


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
