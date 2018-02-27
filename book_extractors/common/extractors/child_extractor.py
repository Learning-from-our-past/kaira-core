import re

from core.pipeline_construction.base_extractor import BaseExtractor
from book_extractors.common.extractors.kaira_id_extractor import KairaIdProvider
from core.utils import regex_utils, text_utils
from core.utils.gender_extract import Gender, GenderException
from core.utils.geo.geocoding import GeoCoder


class CommonChildExtractor(BaseExtractor):
    geocoder = GeoCoder()
    extraction_key = 'children'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(CommonChildExtractor, self).__init__(cursor_location_depends_on, options)
        self._kaira_id_provider = KairaIdProvider()

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)

        children_results = self._find_children(entry['text'], start_position)
        return self._add_to_extraction_results(children_results[0], extraction_results, extraction_metadata, children_results[1])

    def _find_children(self, text, start_position):
        cursor_location = start_position
        text = re.sub(r"sekä", ",", text)
        children_entries = []

        try:
            found_children_match = regex_utils.safe_search(self.CHILD_PATTERN, text, self.CHILD_OPTIONS)
            cursor_location = found_children_match.end()
            children_str = found_children_match.group("children")
            cleaned_children = self._clean_children(children_str)
            children_entries = self._split_children(cleaned_children)

        except regex_utils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('childrenNotFound', 5)

        return children_entries, cursor_location

    @staticmethod
    def _clean_children(children_str):
        children_str = children_str.strip(",")
        children_str = children_str.strip(".")
        children_str = children_str.strip()
        return children_str

    def _split_children(self, children_str):
        found_children_matches = regex_utils.regex_iter(self.SPLIT_PATTERN1, children_str, self.SPLIT_OPTIONS1)
        children_entries = []
        for m in found_children_matches:
            # check if there is "ja" word as separator such as "Seppo -41 ja Jaakko -32.
            ja_word = regex_utils.search(r"\sja\s", m.group("child"))
            if ja_word is not None:
                first_child = self._process_child(m.group("child")[0:ja_word.start()])
                second_child = self._process_child(m.group("child")[ja_word.end():])

                if first_child is not None and second_child is not None:
                    self._twins_year_handler(first_child, second_child)
                    children_entries.append(first_child)
                    children_entries.append(second_child)
                elif first_child is not None:
                    children_entries.append(first_child)
                elif second_child is not None:
                    children_entries.append(second_child)

            else:
                child = self._process_child(m.group("child"))
                if child is not None:
                    children_entries.append(child)

        return children_entries

    @staticmethod
    def _twins_year_handler(first, second):
        # if there is twins, the book doesn't explicitly define birthyear for first one.
        # therefore copy second child's value to first one
        if first is not None and second is not None:
            if first["birthYear"] is None and second["birthYear"] is not None:
                first["birthYear"] = second["birthYear"]

    def _process_child(self, child):
        try:
            name = regex_utils.safe_search(self.NAME_PATTERN, child, self.CHILD_OPTIONS).group("name")
            name = name.strip()
            name = name.strip("-")
            name = name.strip(" ")
            try:
                gender = Gender.find_gender(name)
            except GenderException:
                self.metadata_collector.add_error_record('genderNotFound', 2)
                gender = None

            try:
                year_match = regex_utils.safe_search(self.YEAR_PATTERN, child, self.CHILD_OPTIONS)
                year = year_match.group("year")
                if float(year) < 70:
                    year = text_utils.int_or_none("19" + year)
                else:
                    year = text_utils.int_or_none("18" + year)
            except regex_utils.RegexNoneMatchException:
                year = None

            return {"name": name, "gender": gender, "birthYear": year, "kairaId": self._kaira_id_provider.get_new_id('C')}
        except regex_utils.RegexNoneMatchException:
            pass
