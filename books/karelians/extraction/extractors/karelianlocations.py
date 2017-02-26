from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import KarelianLocationException
from shared import regexUtils
import re
from shared.geo.geocoding import GeoCoder, LocationNotFound

class KarelianLocationsExtractor(BaseExtractor):
    """ Tries to extract the locations of the person in karelia.
    """
    geocoder = GeoCoder()
    KARELIAN_REGION_ID = 'karelia'

    def extract(self, text, entry):
        self.LOCATION_PATTERN = r"Asuinp{s<=1}\.?,?\s?(?:Karjalassa){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=\.?\s(Muut))" # r"Muut\.?,?\s?(?:asuinp(\.|,)){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=—)"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.SPLIT_PATTERN1 = r"(?P<place>[A-ZÄ-Öa-zä-ö-]+)\s?(?P<years>[\d,\.\s—-]*)" # r"(?P<place>[A-ZÄ-Öa-zä-ö\s-]+)\s(?P<years>[\d,\.\s—-]*)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)
        self.coordinates_notfound = False   # used to limit error logging to only single time
        self.returned = ""
        self.locations = ""
        self.location_listing = []
        self.location_error = False
        self._find_locations(text)

        return self._constructReturnDict()

    def _find_locations(self, text):
        try:
            found_locations = regexUtils.safeSearch(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            self.matchFinalPosition = found_locations.end()
            self.locations = found_locations.group("asuinpaikat")
            self._clean_locations()
            self._split_locations()
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(KarelianLocationException.eType, self.currentChild)
            self.location_error = KarelianLocationException.eType

    def _clean_locations(self):
        self.locations = self.locations.strip(",")
        self.locations = self.locations.strip(".")
        self.locations = self.locations.strip()

        self.locations = re.sub(r"([a-zä-ö])(?:\s|\-)([a-zä-ö])", r"\1\2", self.locations)

        self.locations = self.locations.lstrip()

    def _split_locations(self):
        found_locations = regexUtils.regexIter(self.SPLIT_PATTERN1, self.locations, self.SPLIT_OPTIONS1)
        count = 0
        for m in found_locations:
            count += 1
            self._process_location(m.group("place"), m.group("years"))
            # print("Place: " + m.group("place") + " Years: " + m.group("years") + " Year count: " + str(self._count_years(m.group("years"))))

        if count == 0:
            self._create_location_entry(self.locations, [])

    def _process_location(self, place, years):

        if self._count_years(years) > 2:
            # split the years
            self._handle_returning_person(place, years)
        else:
            move_years = self._get_move_years(years)
            self._create_location_entry(place, move_years)

    def _handle_returning_person(self, place, years):
        """This function simply creates recursively a duplicate location with new years"""
        # split years
        year_units = re.split(r"[,\.]", years)

        if len(year_units) > 1:
            # call algorithm recursively to each one
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
        # create the final entry
        moved_out = ""
        moved_in = ""
        geocoordinates = {"latitude" : "", "longitude": ""}
        if len(move_years) == 1:
            moved_out = move_years[0]
        if len(move_years) == 2:
            moved_out = move_years[1]
            moved_in = move_years[0]


        try:
            geocoordinates = self.geocoder.get_coordinates(place, "russia")
        except LocationNotFound:
            if not self.coordinates_notfound:
                self.coordinates_notfound = True
                #self.errorLogger.logError(LocationNotFound.eType, self.currentChild )

        try:
            if int(moved_in) >= 41 and int(moved_in) <= 43:
                self.returned = True
        except ValueError:
            pass

        self.location_listing.append(ValueWrapper({
            KEYS["karelianlocation"]: ValueWrapper(place),
            KEYS["kareliancoordinate"]: ValueWrapper({
                KEYS["latitude"]: ValueWrapper(geocoordinates["latitude"]),
                KEYS["longitude"]: ValueWrapper(geocoordinates["longitude"])
            }),
            KEYS["movedOut"]: ValueWrapper(moved_out),
            KEYS["movedIn"]: ValueWrapper(moved_in),
            KEYS["region"]: self.KARELIAN_REGION_ID}))


    def _count_years(self, text):
        years = regexUtils.regexIter(r"\d\d", text, self.SPLIT_OPTIONS1)
        return len(list(years))

    def _constructReturnDict(self):
        loc = ValueWrapper(self.location_listing)
        loc.error = self.location_error
        return {KEYS["karelianlocations"]: loc,
                KEYS["returnedkarelia"]: ValueWrapper(self.returned),
                KEYS["karelianlocationsCount"]: ValueWrapper(len(self.location_listing))}
