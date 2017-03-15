import re

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import StopExtractionException
from shared import regexUtils
from shared.genderExtract import Gender
from shared.genderExtract import GenderException
from shared.geo.geocoding import GeoCoder, LocationNotFound

Gender.load_names()


class ChildExtractor(BaseExtractor):
    geocoder = GeoCoder()

    def __init__(self, key_of_cursor_location_dependent, options):
        super(ChildExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.CHILD_PATTERN = r"(?:Lapset|tytär|poika)(;|:)(?P<children>.*?)Asuinp{s<=1}"
        self.CHILD_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.MANY_MARRIAGE_PATTERN = r"(toisesta|ensimmäisestä|aikaisemmasta|edellisestä|nykyisestä|avioliitosta)"

        self.SPLIT_PATTERN1 = r"(?P<child>[A-ZÄ-Öa-zä-ö\d\s-]{3,})"
        self.NAME_PATTERN = r"^(?P<name>[a-zä-ö\s-]+)"
        self.YEAR_PATTERN = r"(?P<year>(\d\d))"
        self.LOCATION_PATTERN = r"\d\d\s(?P<location>[a-zä-ö\s-]+$)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        results = self._find_children(entry['text'])

        return self._constructReturnDict({
            KEYS["manymarriages"]: results[1], KEYS["children"]: results[0]
        }, extraction_results, results[2])

    def _find_children(self, text):
        children = []
        cursor_location = 0
        many_marriages = False
        try:
            found_children = regexUtils.safeSearch(self.CHILD_PATTERN, text, self.CHILD_OPTIONS)
            cursor_location = found_children.end()
            children_str = found_children.group("children")
            many_marriages = self._check_many_marriages(children_str)
            children_str = self._clean_children(children_str)
            children = self._split_children(children_str)

        except regexUtils.RegexNoneMatchException as e:
            pass
            # TODO: Metadata logging here: self.errorLogger.logError(NoChildrenException.eType, self.currentChild)

        return children, many_marriages, cursor_location

    def _check_many_marriages(self, text):
        marriage = regexUtils.search(self.MANY_MARRIAGE_PATTERN, text, self.CHILD_OPTIONS)
        # TODO: metadata logging here: self.errorLogger.logError(MultipleMarriagesException.eType, self.currentChild)
        return marriage is not None

    @staticmethod
    def _clean_children(children_str):
        children_str = children_str.strip(",")
        children_str = children_str.strip(".")
        children_str = children_str.strip()
        return children_str

    def _split_children(self, children_str):
        found_children = regexUtils.regexIter(self.SPLIT_PATTERN1, children_str, self.SPLIT_OPTIONS1)
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

        name = regexUtils.safeSearch(self.NAME_PATTERN, child, self.CHILD_OPTIONS).group("name")
        name = name.strip()
        name = name.strip("-")
        name = name.strip(" ")

        try:
            gender = Gender.find_gender(name)
        except GenderException as e:
            # TODO: metadata logging here: self.errorLogger.logError(e.eType, self.currentChild)
            gender = ""

        try:
            year_match = regexUtils.safeSearch(self.YEAR_PATTERN, child, self.CHILD_OPTIONS)
            year = year_match.group("year")
            if float(year) <70:
                year = "19" + year
            else:
                year = "18" + year
        except regexUtils.RegexNoneMatchException:
            year = ""

        try:
            loc_match = regexUtils.safeSearch(self.LOCATION_PATTERN, child, self.CHILD_OPTIONS)
            location = loc_match.group("location")
            location = location.strip()
            location = location.strip("-")
            coordinates = self._find_birth_coord(location)
        except regexUtils.RegexNoneMatchException:
            location = ""
            coordinates = self.geocoder.get_empty_coordinates()

        return {KEYS["childName"]: name,
                KEYS["gender"]: gender,
                KEYS["birthYear"]: year,
                KEYS["childLocationName"]: location,
                KEYS["childCoordinates"]: {
                    KEYS["latitude"]: coordinates["latitude"],
                    KEYS["longitude"]: coordinates["longitude"]}
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
