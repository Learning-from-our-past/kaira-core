from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.farmers.extraction.extractionExceptions import OtherLocationException
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
        self.LOCATION_PATTERN = r"Muut\.?,?\s?(?:asuinp(\.|,)?){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=—)" #r"Muut\.?,?\s?(?:asuinp(\.|,)?){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*?)(?=[A-Za-zÄ-Öä-ö\s\.]{30,50})" # #r"Muut\.?,?\s?(?:asuinp(\.|,)){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-])*(?=—\D\D\D)"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.SPLIT_PATTERN1 = r"(?P<place>[A-ZÄ-Öa-zä-ö-]+)\s?(?P<years>[\d,\.\s—-]*)" #r"(?P<place>[A-ZÄ-Öa-zä-ö\s-]+)\s(?P<years>[\d,\.\s—-]*)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)
        self.LOCATION_THRESHOLD = 3
        self.coordinates_notfound_threshold = self.LOCATION_THRESHOLD   #used to detect when the locations end. To remove noplace words.
        self.locations = ""
        self.locationlisting = []

        try:
            self._find_locations(text)
        except LocationThresholdException:
            pass

        return self._constructReturnDict()

    def _find_locations(self, text):

        try:
            foundLocations = regexUtils.safeSearch(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            self.matchFinalPosition = foundLocations.end()
            self.locations = foundLocations.group("asuinpaikat")
            if self.locations is None:
                raise regexUtils.RegexNoneMatchException("asd")
            self._clean_locations()

            self._split_locations()
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(OtherLocationException.eType, self.currentChild)

    def _clean_locations(self):
        self.locations = self.locations.strip(",")
        self.locations = self.locations.strip(".")
        self.locations = self.locations.strip()
        self.locations = re.sub(r"([a-zä-ö])(?:\s|\-)([a-zä-ö])", r"\1\2", self.locations)
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
            if self.coordinates_notfound_threshold > 0:
                self._create_location_entry(place, move_years)
            else:
                self.locationlisting = self.locationlisting[:-3]
                raise LocationThresholdException()

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
        print(place)
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
            self.coordinates_notfound_threshold = self.LOCATION_THRESHOLD
        except LocationNotFound as e:
            self.coordinates_notfound_threshold -= 1
            #self.errorLogger.logError(LocationNotFound.eType, self.currentChild )

        self.locationlisting.append(ValueWrapper({KEYS["otherlocation"] : ValueWrapper(place), KEYS["othercoordinate"] : ValueWrapper({"latitude": ValueWrapper(geocoordinates["latitude"]), "longitude": ValueWrapper(geocoordinates["longitude"])}), "movedOut" : ValueWrapper(movedOut), "movedIn" : ValueWrapper(movedIn)}))

    def _count_years(self, text):
        years = regexUtils.regexIter(r"\d\d", text, self.SPLIT_OPTIONS1)
        return len(list(years))

    def _constructReturnDict(self):
        return {KEYS["otherlocations"] : ValueWrapper(self.locationlisting), KEYS["otherlocationsCount"] : ValueWrapper(len(self.locationlisting))}

class LocationThresholdException(Exception):
    message = "Locations couldn't be found from db"
    def __unicode__(self):
        return repr(self.message)
