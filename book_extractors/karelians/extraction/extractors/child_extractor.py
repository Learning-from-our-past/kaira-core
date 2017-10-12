import re

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.common.extractors.kaira_id_extractor import KairaIdProvider
from book_extractors.extraction_exceptions import StopExtractionException
from shared import regexUtils, text_utils
from shared.gender_extract import Gender
from shared.gender_extract import GenderException
from shared.geo.geocoding import GeoCoder, LocationNotFound
from book_extractors.common.postprocessors import place_name_cleaner

Gender.load_names()


class ChildExtractor(BaseExtractor):
    geocoder = GeoCoder()
    extraction_key = 'children'

    def __init__(self, key_of_cursor_location_dependent, options, dependencies_contexts=None):
        super(ChildExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self._kaira_id_provider = KairaIdProvider()
        self.CHILD_PATTERN = r"(?:Lapset|tytär|poika)(;|:)(?P<children>.*?)Asuinp{s<=1}"
        self.CHILD_OPTIONS = (re.UNICODE | re.IGNORECASE)

        self.SPLIT_PATTERN1 = r"(?P<child>[A-ZÄ-Öa-zä-ö\d\s-]{3,})"
        self.NAME_PATTERN = r"^(?P<name>[a-zä-ö\s-]+)"
        self.YEAR_PATTERN = r"(?P<year>(\d\d))"
        self.LOCATION_PATTERN = r"\d\d\s(?P<location>[a-zä-ö\s-]+$)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        children_results = self._find_children(entry['text'])

        return self._add_to_extraction_results(children_results[0], extraction_results, extraction_metadata, children_results[1])

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        """
        Add location information to each child in this postprocess method.
        :param entry: 
        :param extraction_results: 
        :return extraction_results: 
        """
        self._get_output_path(extraction_results)[self.extraction_key] = self._augment_location_data_of_children(self._get_output_path(extraction_results)[self.extraction_key])
        return extraction_results, extraction_metadata

    def _augment_location_data_of_children(self, children):
        for child in children:
            location_entry = {
                KEYS['locationName']: child[KEYS["childLocationName"]],
                KEYS['region']: None,
            }

            location_entry = place_name_cleaner.clean_place_name(location_entry)
            child[KEYS["childLocationName"]] = place_name_cleaner.try_to_normalize_place_name(location_entry, self.metadata_collector)

            coordinates = self._find_birth_coord(child[KEYS["childLocationName"]][KEYS['locationName']])
            location_entry[KEYS["childCoordinates"]] = {
                KEYS["latitude"]: coordinates["latitude"],
                KEYS["longitude"]: coordinates["longitude"]
            }

        return children

    def _find_children(self, text):
        children = []
        cursor_location = 0
        try:
            found_children = regexUtils.safe_search(self.CHILD_PATTERN, text, self.CHILD_OPTIONS)
            cursor_location = found_children.end()
            children_str = found_children.group("children")
            children_str = self._clean_children(children_str)
            children = self._split_children(children_str)

        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('childrenNotFound', 5)

        return children, cursor_location

    @staticmethod
    def _clean_children(children_str):
        children_str = children_str.strip(",")
        children_str = children_str.strip(".")
        children_str = children_str.strip()
        return children_str

    def _split_children(self, children_str):
        found_children = regexUtils.regex_iter(self.SPLIT_PATTERN1, children_str, self.SPLIT_OPTIONS1)
        children = []
        for m in found_children:
            try:
                children.append(self._process_child(m.group("child"), children))
            except (regexUtils.RegexNoneMatchException, StopExtractionException):
                pass

        return children

    def _process_child(self, child, child_list):
        birth_loc = regexUtils.search("syntyneet{s<=1}\s(?P<location>\w*)", child, self.CHILD_OPTIONS)
        if birth_loc is not None:
            # found a "Syntyneet <place>" string. Set it to the previous children.
            for c in child_list:
                if c[KEYS["childLocationName"]] == "":
                    c[KEYS["childLocationName"]] = birth_loc.group("location")
            raise StopExtractionException('Child extraction should be stopped here. Current child is not valid child.')

        name = regexUtils.safe_search(self.NAME_PATTERN, child, self.CHILD_OPTIONS).group("name")
        name = name.strip()
        name = name.strip("-")
        name = name.strip(" ")

        try:
            gender = Gender.find_gender(name)
        except GenderException:
            self.metadata_collector.add_error_record('genderNotFound', 2)
            gender = None

        try:
            year_match = regexUtils.safe_search(self.YEAR_PATTERN, child, self.CHILD_OPTIONS)
            year = year_match.group("year")
            if float(year) < 70:
                year = "19" + year
            else:
                year = "18" + year
        except regexUtils.RegexNoneMatchException:
            year = ""

        try:
            loc_match = regexUtils.safe_search(self.LOCATION_PATTERN, child, self.CHILD_OPTIONS)
            location = loc_match.group("location")
            location = location.strip()
            location = location.strip("-")
        except regexUtils.RegexNoneMatchException:
            location = ""

        return {KEYS["childName"]: name,
                KEYS["gender"]: gender,
                KEYS["birthYear"]: text_utils.int_or_none(year),
                KEYS["childLocationName"]: location,
                KEYS["kairaId"]: self._kaira_id_provider.get_new_id('C')
                }

    def _find_birth_coord(self, location_name):
        try:
            geocoordinates = self.geocoder.get_coordinates(location_name, "finland")
        except LocationNotFound as e:
            try:
                geocoordinates = self.geocoder.get_coordinates(location_name, "russia")
            except LocationNotFound as e:
                return self.geocoder.get_empty_coordinates()
        return geocoordinates
