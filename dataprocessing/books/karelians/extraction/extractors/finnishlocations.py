from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import OtherLocationException
from shared import regexUtils
from shared import textUtils
import re
import regex
from shared.geo.geocoding import GeoCoder, LocationNotFound

class FinnishLocationsExtractor(BaseExtractor):
    """ Tries to extract the locations of the person in karelia.
    """
    geocoder = GeoCoder()

    def extract(self, text, entry):
        self.LOCATION_PATTERN = r"Muut\.?,?\s?(?:asuinp(\.|,)){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=—)"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.SPLIT_PATTERN1 = r"(?P<place>[A-ZÄ-Öa-zä-ö-]+)\s?(?P<years>[\d,\.\s—-]*)" #r"(?P<place>[A-ZÄ-Öa-zä-ö\s-]+)\s(?P<years>[\d,\.\s—-]*)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)
        self.coordinates_notfound = False   #used to limit error logging to only single time
        self.locations = ""
        self.locationlisting = []
        self._find_locations(text)

        return self._constructReturnDict()

    def _find_locations(self, text):
        try:
            foundLocations = regexUtils.safeSearch(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            self.matchFinalPosition = foundLocations.end()
            self.locations = foundLocations.group("asuinpaikat")
            self._clean_locations()
            self._split_locations()
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(OtherLocationException.eType, self.currentChild)

    def _clean_locations(self):
        self.locations = self.locations.strip(",")
        self.locations = self.locations.strip(".")
        self.locations = self.locations.strip()
        self.locations = self.locations.lstrip()

    def _split_locations(self):
        foundLocations = regexUtils.regexIter(self.SPLIT_PATTERN1, self.locations, self.SPLIT_OPTIONS1)
        count = 0
        for m in foundLocations:

            count += 1
            self._process_location(m.group("place"), m.group("years"))
            #print("Place: " + m.group("place") + " Years: " + m.group("years") + " Year count: " + str(self._count_years(m.group("years"))))

        if count == 0:
            self._create_location_entry(self.locations, [])

    def _process_location(self, place, years):

        if self._count_years(years) > 2:
            #split the years and mark the return to Karelia
            self._handle_returning_person(place, years)
        else:
            move_years = self._get_move_years(years)
            self._create_location_entry(place, move_years)

    def _handle_returning_person(self, place, years):
        """This function simply creates recursively a duplicate location with new years"""
        #split years
        year_units = re.split(r"[,\.]", years)

        if len(year_units) > 1:
            #call algorithm recursively to each one
            for y in year_units:
                if len(y.strip()) > 1:
                    self._process_location(place, y)


    def _get_move_years(self, yearstr):
        yearsm = regexUtils.regexIter(r"(?P<year>\d\d)", yearstr, self.SPLIT_OPTIONS1)
        y = []
        for m in yearsm:
            y.append(m.group("year"))
        if len(y) == 0:
            y = [""]
        return y

    def _create_location_entry(self, place, move_years):
        place = place.strip()
        #create the final(?) entry
        movedOut = ""
        movedIn = ""
        geocoordinates = {"latitude" : "", "longitude": ""}
        if len(move_years) == 1:
            movedOut = move_years[0]
        if len(move_years) == 2:
            movedOut = move_years[1]
            movedIn = move_years[0]


        try:
            geocoordinates = self.geocoder.get_coordinates(place, "finland")
        except LocationNotFound as e:
            if not self.coordinates_notfound:
                self.coordinates_notfound = True
                #self.errorLogger.logError(LocationNotFound.eType, self.currentChild )

        self.locationlisting.append(ValueWrapper({KEYS["otherlocation"] : ValueWrapper(place), KEYS["othercoordinate"] : ValueWrapper({"latitude": ValueWrapper(geocoordinates["latitude"]), "longitude": ValueWrapper(geocoordinates["longitude"])}), "movedOut" : ValueWrapper(movedOut), "movedIn" : ValueWrapper(movedIn)}))


    def _count_years(self, text):
        years = regexUtils.regexIter(r"\d\d", text, self.SPLIT_OPTIONS1)
        return len(list(years))

    def _constructReturnDict(self):
        return {KEYS["otherlocations"] : ValueWrapper(self.locationlisting)}
