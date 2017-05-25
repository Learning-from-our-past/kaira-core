from book_extractors.processdata import ProcessData
from book_extractors.karelians.resultcsvbuilder import ResultCsvBuilder
from book_extractors.karelians.resultjsonbuilder import ResultJsonBuilder
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.name_extractor import NameExtractor
from book_extractors.karelians.extraction.extractors.original_family_extractor import OrigFamilyExtractor
from book_extractors.karelians.extraction.extractors.profession_extractor import ProfessionExtractor
from book_extractors.karelians.extraction.extractors.image_extractor import ImageExtractor
from book_extractors.karelians.extraction.extractors.omakotitalo_extractor import OmakotitaloExtractor
from book_extractors.karelians.extraction.extractors.birthday_extractor import BirthdayExtractor
from book_extractors.karelians.extraction.extractors.location_extractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.migration_route_extractors import MigrationRouteExtractor
from book_extractors.karelians.extraction.extractors.spouse_extractor import SpouseExtractor
from book_extractors.karelians.extraction.extractors.child_extractor import ChildExtractor
from shared.gender_extract import Gender


class KarelianBooksExtractor:

    def __init__(self, update_callback):
        Gender.load_names()
        self._extractor_pipeline = self._define_extraction_pipeline()
        self._extractor = ProcessData(self._extractor_pipeline, update_callback)
        self._results = None

    def _define_extraction_pipeline(self):
        pipeline_components = [
            configure_extractor(NameExtractor),
            configure_extractor(ImageExtractor),
            configure_extractor(OrigFamilyExtractor),
            configure_extractor(ProfessionExtractor, depends_on_match_position_of_extractor=OrigFamilyExtractor),
            configure_extractor(BirthdayExtractor, depends_on_match_position_of_extractor=OrigFamilyExtractor),
            configure_extractor(BirthdayLocationExtractor, depends_on_match_position_of_extractor=BirthdayExtractor),
            configure_extractor(MigrationRouteExtractor),
            configure_extractor(OmakotitaloExtractor),
            configure_extractor(SpouseExtractor),
            configure_extractor(ChildExtractor)
        ]

        return ExtractionPipeline(pipeline_components)

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
