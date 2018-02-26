# -*- coding: utf-8 -*-
import re

from book_extractors.common.extraction_keys import KEYS
from core.base_extractor import BaseExtractor
from book_extractors.common.extractors.kaira_id_extractor import KairaIdProvider
from core.utils import regex_utils


class SpouseExtractor(BaseExtractor):
    extraction_key = 'spouse'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(SpouseExtractor, self).__init__(cursor_location_depends_on, options)
        self.kaira_id_provider = KairaIdProvider()

        self.PATTERN = r'Puol\.?,?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp))'
        self.NAMEPATTERN = r'(?P<name>^[\w\s-]*)'
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        result, cursor_location = self._find_spouse(entry, start_position)

        return self._add_to_extraction_results(result, extraction_results, extraction_metadata, cursor_location=cursor_location)

    def _find_spouse(self, entry, start_position):
        cursor_location = start_position
        spouse_data = None

        try:
            found_spouse_match = regex_utils.safe_search(self.PATTERN, entry['text'], self.OPTIONS)
            spouse_data = self._find_spouse_data(found_spouse_match.group('spousedata'), entry)

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = found_spouse_match.end() + start_position - 4
        except regex_utils.RegexNoneMatchException:
            pass

        return spouse_data, cursor_location

    def _find_spouse_data(self, sub_text, entry):
        spouse_name = ''
        spouse_details = None

        try:
            spouse_name_match = regex_utils.safe_search(self.NAMEPATTERN, sub_text, self.OPTIONS)
            spouse_name = spouse_name_match.group('name').strip()
            spouse_name = re.sub(r'\so$', '', spouse_name)
            spouse_details, metadata = self._find_spouse_details(sub_text[spouse_name_match.end() - 2:],
                                                                 entry['full_text'])
            spouse_details = spouse_details['spouse']

            # FIXME: This will break when adding new extractors to YAML configuration
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
                KEYS['kairaId']: self.kaira_id_provider.get_new_id('S'),
                'warData': spouse_details['warData'],
                'marttaActivityFlag': spouse_details['marttaActivityFlag']
            }

        except regex_utils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('spouseNotFound', 6)

        return spouse_name, spouse_details

    def _find_spouse_details(self, text, full_text):
        return self._sub_extraction_pipeline.process({'text': text, 'full_text': full_text})
