from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import NoChildrenException
from shared import regexUtils
from shared import textUtils
import re
import regex
from shared.geo.geocoding import GeoCoder, LocationNotFound

class ChildExtractor(BaseExtractor):
    geocoder = GeoCoder()

    def extract(self, text, entry):

        self.CHILD_PATTERN = r"(?:Lapset|tytär|poika)(;|:)(?P<children>.*?)Asuinp{s<=1}"
        self.CHILD_OPTIONS = (re.UNICODE | re.IGNORECASE)

        self.SPLIT_PATTERN1 = r"(?P<child>[A-ZÄ-Öa-zä-ö\d\s-]{3,})"
        self.NAME_PATTERN = r"^(?P<name>[a-zä-ö\s-]+)"
        self.YEAR_PATTERN = r"(?P<year>(\d\d))"
        self.LOCATION_PATTERN = r"\d\d\s(?P<location>[a-zä-ö\s-]+$)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)
        self.children_str = ""
        self.child_list = []
        self._find_children(text)
        return self._constructReturnDict()

    def _find_children(self, text):
        try:
            foundChildren= regexUtils.safeSearch(self.CHILD_PATTERN, text, self.CHILD_OPTIONS)
            self.matchFinalPosition = foundChildren.end()
            self.children_str = foundChildren.group("children")

            self._clean_children()
            self._split_children()

        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(NoChildrenException.eType, self.currentChild)

    def _clean_children(self):
        self.children_str = self.children_str.strip(",")
        self.children_str = self.children_str.strip(".")
        self.children_str = self.children_str.strip()

    def _split_children(self):
        print(self.children_str)
        foundChildren = regexUtils.regexIter(self.SPLIT_PATTERN1, self.children_str, self.SPLIT_OPTIONS1)
        count = 0
        for m in foundChildren:
            count += 1
            self._process_child(m.group("child"))
            #print("Place: " + m.group("place") + " Years: " + m.group("years") + " Year count: " + str(self._count_years(m.group("years"))))



    def _process_child(self, child):
        #check if syntyneet flag:
        birthLoc = regexUtils.search("syntyneet{s<=1}\s(?P<location>\w*)", child, self.CHILD_OPTIONS)
        if birthLoc is not None:
            #found a "Syntyneet <place>" string. Set it to the previous children.
            for c in self.child_list:
                if c.value["locationName"].value == "":
                    c.value["locationName"].value = birthLoc.group("location")
            return

        if child.find("Syntyneet") != -1:
            print("SYNTYNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEET")
        try:
            name = regexUtils.safeSearch(self.NAME_PATTERN, child, self.CHILD_OPTIONS).group("name")
            name = name.strip()
            name = name.strip("-")
            try:
                yearMatch = regexUtils.safeSearch(self.YEAR_PATTERN, child, self.CHILD_OPTIONS)
                year = yearMatch.group("year")
            except regexUtils.RegexNoneMatchException:
                year = ""

            try:
                locMatch = regexUtils.safeSearch(self.LOCATION_PATTERN, child, self.CHILD_OPTIONS)
                location = locMatch.group("location")
                location = location.strip()
                location = location.strip("-")
                coordinates = self._find_birth_coord(location)
            except regexUtils.RegexNoneMatchException:
                location = ""
                coordinates = self.geocoder.get_empty_coordinates()

            self.child_list.append(ValueWrapper({"name" : ValueWrapper(name), "birthYear" : ValueWrapper(year),
                                                 "locationName" : ValueWrapper(location),
                                                 "childCoordinates" : ValueWrapper({"latitude": ValueWrapper(coordinates["latitude"]), "longitude": ValueWrapper(coordinates["longitude"])})}))
        except regexUtils.RegexNoneMatchException:
            pass


    def _find_birth_coord(self, location_name):
        try:
            geocoordinates = self.geocoder.get_coordinates(location_name, "finland")
        except LocationNotFound as e:
            try:
                geocoordinates = self.geocoder.get_coordinates(location_name, "russia")
            except LocationNotFound as e:
                return self.geocoder.get_empty_coordinates()
        return geocoordinates



    def _constructReturnDict(self):
        """KEYS["karelianlocations"] : ValueWrapper(self.locationlisting),
                KEYS["returnedkarelia"] : ValueWrapper(self.returned),
                KEYS["karelianlocationsCount"] : ValueWrapper(len(self.locationlisting))"""
        return {KEYS["children"] : ValueWrapper(self.child_list), KEYS["childCount"] : ValueWrapper(len(self.child_list))}
