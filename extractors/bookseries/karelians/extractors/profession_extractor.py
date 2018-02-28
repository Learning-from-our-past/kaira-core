import re

import core.utils.regex_utils as regexUtils
from core.utils import text_utils
import csv
from core.pipeline_construction.base_extractor import BaseExtractor


class ProfessionExtractor(BaseExtractor):
    SEARCH_SPACE = 60
    extraction_key = 'profession'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(ProfessionExtractor, self).__init__(cursor_location_depends_on, options)
        self.PROFESSION_PATTERN = r"(?<profession>[a-zä-ö,\. ]*) synt"
        self.PROFESSION_OPTIONS = (re.UNICODE | re.IGNORECASE)

        def cast_int(value):
            try:
                return int(value)
            except ValueError:
                return None

        with open('support_datasheets/occupations.csv', 'r', encoding='utf-8') as occupations_list:
            occupations = list(csv.DictReader(occupations_list))
            self._occupation_extra_data = {}

            for occupation in occupations:
                self._occupation_extra_data[occupation['professionName']] = {
                    'englishName': occupation['professionEnglishName'],
                    'agricultureOrForestryRelated': bool(occupation['agricultureOrForestryRelated']),
                    'manualLabor': bool(occupation['manualLabor']),
                    'education': bool(occupation['education']),
                    'SESgroup1989': cast_int(occupation['SESgroup1989']),
                    'occupationCategory': cast_int(occupation['occupationCategory']),
                    'socialClassRank': cast_int(occupation['socialClassRank'])
                }

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        profession_results = self._get_profession(entry['text'], start_position)

        return self._add_to_extraction_results(profession_results[0], extraction_results, extraction_metadata, profession_results[1])

    def _get_profession(self, text, start_position):
        profession_name, cursor_location = self._find_profession(text, start_position)
        return self._add_profession_extra_information(profession_name), cursor_location

    def _add_profession_extra_information(self, profession_name):
        profession_output = {
            'professionName': profession_name,
            'extraInfo': None
        }

        if profession_name in self._occupation_extra_data:
            profession_output['extraInfo'] = self._occupation_extra_data[profession_name]

        return profession_output

    def _find_profession(self, text, start_position):
        text = text_utils.take_sub_str_based_on_range(text, start_position, self.SEARCH_SPACE)
        cursor_location = 0
        profession = None

        try:
            # limit the search range if there is spouse keyword:
            try:
                found_spouse_word = regexUtils.safe_search(r"Puol", text, self.PROFESSION_OPTIONS)
                text = text_utils.take_sub_str_based_on_range(text, 0, found_spouse_word.start())
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
