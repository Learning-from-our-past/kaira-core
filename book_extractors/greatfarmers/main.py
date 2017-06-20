from book_extractors.processdata import ProcessData
from book_extractors.greatfarmers.resultcsvbuilder import ResultCsvBuilder
from book_extractors.greatfarmers.resultjsonbuilder import ResultJsonBuilder
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.greatfarmers.extraction.extractors.metadata_extractor import MetadataExtractor
from book_extractors.greatfarmers.extraction.extractors.owner_extractor import OwnerExtractor
from book_extractors.greatfarmers.extraction.extractors.child_extractor import ChildExtractor
from book_extractors.greatfarmers.extraction.extractors.farm_extractor import FarmExtractor
from book_extractors.greatfarmers.extraction.extractors.bool_extractor import BoolExtractor
from book_extractors.greatfarmers.extraction.extractors.quantity_extractor import QuantityExtractor
from book_extractors.greatfarmers.extraction.extractors.spouse_extractor import SpouseExtractor
from book_extractors.common.extractors.kaira_id_extractor import KairaIdExtractor
from book_extractors.common.extractors.previous_marriages_flag_extractor import PreviousMarriagesFlagExtractor
from shared.gender_extract import Gender
from book_extractors.common.extraction_keys import KEYS
import book_extractors.extraction_constants as extraction_constants

BOOK_SERIES_ID = 'suuretmaatilat'    # Used to identify this book series in xml files

class GreatFarmersBooksExtractor:

    def __init__(self, update_callback):
        Gender.load_names()
        self._extractor_pipeline = self._define_extraction_pipeline()
        self._extractor = ProcessData(self._extractor_pipeline, update_callback)
        self._results = None

    @staticmethod
    def _define_extraction_pipeline():
        # TODO: Maybe create separate classes with these definitions which then call boolean extractor with these patterns?
        boolean_flag_patterns = {
            KEYS["oat"]: r"(kaura(?!nen))",
            KEYS["barley"]: r"ohra",
            KEYS["hay"]: r"(heinä(?!mäki))",
            KEYS["potatoes"]: r"peruna",
            KEYS["wheat"]: r"vehnä",
            KEYS["rye"]: r"ruis",
            KEYS["sugarbeet"]: r"sokerijuuri",
            KEYS["lanttu"]: r"lanttu",
            KEYS["puimakone"]: r"puimakone",
            KEYS["tractor"]: r"traktori",
            KEYS["horse"]: r"hevonen|hevos",
            KEYS["chicken"]: r"kanoja|\skanaa",
            KEYS["siirtotila"]: r"siirtotila",
            KEYS["kantatila"]: r"kantatila",
            KEYS["moreeni"]: r"moreeni",
            KEYS["hiesu"]: r"hiesu",
            KEYS["hieta"]: r"(hieta(?!nen))",
            KEYS["muta"]: r"muta",
            KEYS["savi"]: r"(savi(?!taipale))",
            KEYS["multa"]: r"multa",
            KEYS["salaojitus"]: r"(salaojitettu|salaojitus)",
            KEYS["talli"]: r"(?!auto)talli",
            KEYS["pine"]: r"mänty(?!nen)",
            KEYS["spruce"]: r"kuusi(?!nen)",
            KEYS["birch"]: r"koivu(?!nen|niem)",
            KEYS["sauna"]: r"sauna",
            KEYS["navetta"]: r"navetta|navetan",
            KEYS["autotalli"]: r"autotalli",
            KEYS["viljankuivuri"]: r"viljankuivuri",
            KEYS["kotitalousmylly"]: r"kotitalousmylly",
            KEYS["ay-karja"]: r"ay-karja",
            KEYS["sk-karja"]: r"sk-karja",
            KEYS["someonedead"]: r"kuoli|kuollut|kaatui|kaatunut",
        }

        quantity_patterns = {
            KEYS["rooms"]: r"(?:(?:asuinhuonetta){s<=1,i<=1}|(?:huonetta){s<=1,i<=1})",
            KEYS["lypsylehma"]: r"(?:(?:lypsävää){s<=1,i<=1}|(?:lypsylehmää){s<=1,i<=1})",
            KEYS["lammas"]: r"(?:(?:(?:lampaita (?:on\s?)?){s<=1,i<=1})|(?:\slammasta))",
            KEYS["lihotussika"]: r"(?:lihotus-?sik){s<=1,i<=1}",
            KEYS["emakko"]: r"(?:(?:(?:emakkoja on\s?){s<=1,i<=1})|(?:\semakkoa))",
            KEYS["nuori"]: r"(?:(?:nuorta){s<=1,i<=1})",
            KEYS["kanoja"]: r"(?:(?:(?:kanoja (?:on\s?)?){s<=1,i<=1})|(?:\skanaa))"
        }

        pipeline_components = [
            configure_extractor(MetadataExtractor),
            configure_extractor(OwnerExtractor),
            configure_extractor(SpouseExtractor),
            configure_extractor(FarmExtractor),
            configure_extractor(ChildExtractor),
            configure_extractor(PreviousMarriagesFlagExtractor),
            configure_extractor(BoolExtractor, extractor_options={'patterns': boolean_flag_patterns}),
            configure_extractor(QuantityExtractor, extractor_options={'patterns': quantity_patterns}),
            configure_extractor(KairaIdExtractor, extractor_options={'bookseries': BOOK_SERIES_ID, 'book_number': extraction_constants.BOOK_NUMBER})
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

