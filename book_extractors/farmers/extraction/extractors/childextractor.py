import re

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared import regexUtils
from shared.genderExtract import Gender, GenderException
from shared.geo.geocoding import GeoCoder


class ChildExtractor(BaseExtractor):
    geocoder = GeoCoder()

    def __init__(self, key_of_cursor_location_dependent, options):
        super(ChildExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.CHILD_PATTERN = r"(?:Lapset|tytär|poika|tyttäret|pojat)(;|:)(?P<children>.*?)(?:\.|Tilal{s<=1}|Edelli{s<=1}|hänen{s<=1}|joka{s<=1}|emännän{s<=1}|isännän{s<=1})"
        self.CHILD_OPTIONS = (re.UNICODE | re.IGNORECASE)

        self.MANY_MARRIAGE_PATTERN = r"(toisesta|ensimmäisestä|aikaisemmasta|edellisestä|nykyisestä|avioliitosta)"
        self.SPLIT_PATTERN1 = r"(?P<child>[A-ZÄ-Öa-zä-ö\d\s-]{3,})"
        self.NAME_PATTERN = r"^(?P<name>[a-zä-ö\s-]+)"
        self.YEAR_PATTERN = r"(?P<year>(\d\d))"
        self.LOCATION_PATTERN = r"\d\d\s(?P<location>[a-zä-ö\s-]+$)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        many_marriages = self._check_many_marriages(entry['text'])

        children_results = self._find_children(entry['text'], start_position)
        return self._constructReturnDict({KEYS["manymarriages"]: many_marriages, KEYS["children"]: children_results[0]}, extraction_results, children_results[1])

    def _find_children(self, text, start_position):
        cursor_location = start_position
        text = re.sub(r"sekä", ",",text)
        children_entries = []

        try:
            found_children_match = regexUtils.safeSearch(self.CHILD_PATTERN, text, self.CHILD_OPTIONS)
            cursor_location = found_children_match.end()
            children_str = found_children_match.group("children")
            cleaned_children = self._clean_children(children_str)
            children_entries = self._split_children(cleaned_children)

        except regexUtils.RegexNoneMatchException as e:
            # TODO: Metadata logging here self.errorLogger.logError(NoChildrenException.eType, self.currentChild)
            pass

        return children_entries, cursor_location

    def _check_many_marriages(self, text):
        marriage = regexUtils.search(self.MANY_MARRIAGE_PATTERN, text, self.CHILD_OPTIONS)
        return marriage is not None

    @staticmethod
    def _clean_children(children_str):
        children_str = children_str.strip(",")
        children_str = children_str.strip(".")
        children_str = children_str.strip()
        return children_str

    def _split_children(self, children_str):
        found_children_matches = regexUtils.regexIter(self.SPLIT_PATTERN1, children_str, self.SPLIT_OPTIONS1)
        children_entries = []
        for m in found_children_matches:
            # check if there is "ja" word as separator such as "Seppo -41 ja Jaakko -32.
            ja_word = regexUtils.search(r"\sja\s", m.group("child"))
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
            if first["birthYear"] == "" and second["birthYear"] != "":
                first["birthYear"] = second["birthYear"]

    def _process_child(self, child):
        try:
            name = regexUtils.safeSearch(self.NAME_PATTERN, child, self.CHILD_OPTIONS).group("name")
            name = name.strip()
            name = name.strip("-")
            name = name.strip(" ")
            try:
                gender = Gender.find_gender(name)
            except GenderException as e:
                # TODO: Metadata logging here self.errorLogger.logError(e.eType, self.currentChild)
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

            return {"name": name, "gender": gender, "birthYear": year}
        except regexUtils.RegexNoneMatchException:
            pass
