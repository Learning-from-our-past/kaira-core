import re

import shared.regexUtils as regexUtils
import shared.textUtils as textUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class ProfessionExtractor(BaseExtractor):
    SEARCH_SPACE = 60
    extraction_key = 'profession'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(ProfessionExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.PROFESSION_PATTERN = r"(?<profession>[a-zä-ö,\. ]*) synt"
        self.PROFESSION_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        profession_results = self._find_profession(entry['text'], start_position)

        return self._add_to_extraction_results(profession_results[0], extraction_results, profession_results[1])

    def _find_profession(self, text, start_position):
        text = textUtils.take_sub_str_based_on_range(text, start_position, self.SEARCH_SPACE)
        cursor_location = 0
        profession = None

        try:
            #limit the search range if there is spouse keyword:
            try:
                found_spouse_word = regexUtils.safe_search(r"Puol", text, self.PROFESSION_OPTIONS)
                text = textUtils.take_sub_str_based_on_range(text, 0, found_spouse_word.start())
            except regexUtils.RegexNoneMatchException as e:
                pass

            found_profession_match = regexUtils.safe_search(self.PROFESSION_PATTERN, text, self.PROFESSION_OPTIONS)

            cursor_location = found_profession_match.end()
            profession = found_profession_match.group("profession")
        except regexUtils.RegexNoneMatchException as e:
            pass

        result_profession = self._clean_professions(profession)

        if result_profession is None:
            self.metadata_collector.add_error_record('professionNotFound', 4)

        return result_profession, cursor_location

    def _clean_professions(self, profession):
        if profession is None:
            return profession

        profession = profession.strip(",")
        profession = profession.strip()
        profession = profession.lstrip()

        uppercase = re.match(r"[A-ZÄ-Ö]", profession)
        if uppercase is not None:
            comma = profession.find(",")
            if comma != -1:
                profession = profession[comma:]

        profession = profession.strip(",")
        profession = profession.strip(".")
        profession = profession.strip()
        profession = profession.lstrip()
        profession = re.sub(r"[a-zä-ö]{1,3}(?:,|\.)\s", "", profession, self.PROFESSION_OPTIONS)

        if len(profession) < 3:
            profession = None

        return profession