# -*- coding: utf-8 -*-
import re

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.birthday_extractor import BirthdayExtractor
from book_extractors.karelians.extraction.extractors.death_extractor import DeathExtractor
from book_extractors.karelians.extraction.extractors.location_extractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.original_family_extractor import FormerSurnameExtractor
from book_extractors.karelians.extraction.extractors.profession_extractor import ProfessionExtractor
from book_extractors.karelians.extraction.extractors.wedding_extractor import WeddingExtractor
from book_extractors.karelians.extraction.extractors.war_data_extractor import WarDataExtractor
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor
from book_extractors.karelians.extraction.extractors.served_during_war_flag_extractor import ServedDuringWarFlagExtractor
from book_extractors.karelians.extraction.extractors.lotta_activity_flag_extractor import LottaActivityFlagExtractor
from book_extractors.karelians.extraction.extractors.martta_activity_flag_extractor import MarttaActivityFlagExtractor
from book_extractors.common.extractors.kaira_id_extractor import KairaIdProvider
from shared import regexUtils


class SpouseExtractor(BaseExtractor):
    extraction_key = 'spouse'

    def __init__(self, key_of_cursor_location_dependent, options, dependencies_contexts=None):
        super(SpouseExtractor, self).__init__(key_of_cursor_location_dependent, options)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(FormerSurnameExtractor),
            configure_extractor(ProfessionExtractor, depends_on_match_position_of_extractor=FormerSurnameExtractor),
            configure_extractor(BirthdayExtractor),
            configure_extractor(BirthdayLocationExtractor, depends_on_match_position_of_extractor=BirthdayExtractor),
            configure_extractor(DeathExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor),
            configure_extractor(WeddingExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor)
        ])

        self._additional_extraction_pipeline = ExtractionPipeline([
            configure_extractor(WarDataExtractor, extractor_options={'in_spouse_extractor': True}),
            configure_extractor(MarttaActivityFlagExtractor,
                                extractor_options={'in_spouse_extractor': True},
                                dependencies_contexts=[('main', 'primaryPerson')])
        ])

        self.kaira_id_provider = KairaIdProvider()

        self.PATTERN = r'Puol\.?,?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp))'
        self.NAMEPATTERN = r'(?P<name>^[\w\s-]*)'
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_results, extraction_metadata)
        parent_data = self._get_parent_data_for_pipeline(extraction_results, extraction_metadata)
        result, cursor_location = self._find_spouse(entry['text'], start_position)
        if result is not None:
            additional_results, additional_metadata = self._additional_extraction_pipeline.process(entry, parent_pipeline_data=parent_data)
            result[WarDataExtractor.extraction_key] = additional_results[WarDataExtractor.extraction_key]
            result[MarttaActivityFlagExtractor.extraction_key] = additional_results[MarttaActivityFlagExtractor.extraction_key]

        return self._add_to_extraction_results(result, extraction_results, extraction_metadata, cursor_location=cursor_location)

    def _find_spouse(self, text, start_position):
        cursor_location = start_position
        spouse_data = None

        try:
            found_spouse_match = regexUtils.safe_search(self.PATTERN, text, self.OPTIONS)
            spouse_data = self._find_spouse_data(found_spouse_match.group('spousedata'))

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = found_spouse_match.end() + start_position - 4
        except regexUtils.RegexNoneMatchException:
            pass

        return spouse_data, cursor_location

    def _find_spouse_data(self, text):
        spouse_name = ''
        spouse_details = None

        try:
            spouse_name_match = regexUtils.safe_search(self.NAMEPATTERN, text, self.OPTIONS)
            spouse_name = spouse_name_match.group('name').strip()
            spouse_name = re.sub(r'\so$', '', spouse_name)
            spouse_details, metadata = self._find_spouse_details(text[spouse_name_match.end() - 2:])

            # Map data to spouse object
            return {
                KEYS['birthData']: {
                    **spouse_details[KEYS['birthData']],
                    KEYS['birthLocation']: spouse_details['birthLocation']
                },
                KEYS['spouseDeathYear']: spouse_details['death'],
                KEYS['formerSurname']: spouse_details['formerSurname'],
                KEYS['spouseProfession']: spouse_details['profession'],
                KEYS['weddingYear']: spouse_details['wedding'],
                KEYS['spouseName']: spouse_name,
                KEYS['hasSpouse']: True,
                KEYS['kairaId']: self.kaira_id_provider.get_new_id('S')
            }

        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('spouseNotFound', 6)

        return spouse_name, spouse_details

    def _find_spouse_details(self, text):
        return self._sub_extraction_pipeline.process({'text': text})
