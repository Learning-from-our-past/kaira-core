from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import KarelianLocationException
from shared import regexUtils
from shared import textUtils
import re

class KarelianLocationsExtractor(BaseExtractor):
    """ Tries to extract the locations of the person in karelia.
    """

    def extract(self, text, entry):
        self.LOCATION_PATTERN = r"Asuinp\.?,?\s?Karjalassa(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9—-]*)(?=\.?\s(Muut))"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.locations = ""
        self._find_locations(text)
        return self._constructReturnDict()

    def _find_locations(self, text):
        try:
            foundLocations= regexUtils.safeSearch(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            self.matchFinalPosition = foundLocations.end()
            self.locations = foundLocations.group("asuinpaikat")
            self._clean_locations()
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(KarelianLocationException.eType, self.currentChild)

    def _clean_locations(self):
        self.locations = self.locations.strip(",")
        self.locations = self.locations.strip()
        self.locations = self.locations.lstrip()

    def _constructReturnDict(self):
        return {KEYS["karelianlocations"] : ValueWrapper(self.locations)}
