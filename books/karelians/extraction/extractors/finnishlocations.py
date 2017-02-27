from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import OtherLocationException
from shared import regexUtils
import re
from shared.geo.geocoding import GeoCoder, LocationNotFound
from books.karelians.extraction.extractors.bnf_parsers import migration_parser

class FinnishLocationsExtractor(BaseExtractor):
    """ Tries to extract the locations of the person in karelia.
    """
    geocoder = GeoCoder()

    OTHER_REGION_ID = 'other'

    def extract(self, text):
        self.LOCATION_PATTERN = r"Muut\.?,?\s?(?:asuinp(\.|,)?){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*—)" #r"Muut\.?,?\s?(?:asuinp(\.|,)?){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*?)(?=[A-Za-zÄ-Öä-ö\s\.]{30,50})" # #r"Muut\.?,?\s?(?:asuinp(\.|,)){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-])*(?=—\D\D\D)"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.SPLIT_PATTERN1 = r"(?P<place>[A-ZÄ-Öa-zä-ö-]+)\s?(?P<years>[\d,\.\s—-]*)" #r"(?P<place>[A-ZÄ-Öa-zä-ö\s-]+)\s(?P<years>[\d,\.\s—-]*)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)
        self.LOCATION_THRESHOLD = 3
        self.coordinates_notfound_threshold = self.LOCATION_THRESHOLD   #used to detect when the locations end. To remove noplace words.
        self.locations = ""
        self.location_listing = []
        self.location_error = False

        try:
            self._find_locations(text)
        except LocationThresholdException:
            pass

        return self._constructReturnDict()

    def _find_locations(self, text):
        # Replace all weird invisible white space characters with regular space
        text = re.sub(r"\s", r" ", text)

        try:
            found_locations = regexUtils.safeSearch(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            self.matchFinalPosition = found_locations.end()
            self.locations = found_locations.group("asuinpaikat")
            self._clean_locations()

            parsed_locations = migration_parser.parse_locations(self.locations)

            for location in parsed_locations:
                self._create_location_entry(location)

        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(OtherLocationException.eType, self.currentChild)
            self.location_error = OtherLocationException.eType

    def _clean_locations(self):
        self.locations = self.locations.strip(",")
        self.locations = self.locations.strip(".")
        self.locations = self.locations.strip()
        self.locations = re.sub(r"([a-zä-ö])(?:\s|\-)([a-zä-ö])", r"\1\2", self.locations)
        self.locations = self.locations.lstrip()

    def _create_location_entry(self, location):
        # If there is municipality information, use it as an main entry name
        village_name = None

        if 'municipality' in location:
            entry_name = location['municipality']
            village_name = location['place']
        else:
            entry_name = location['place']

        def get_coordinates_by_name(place_name):
            try:
                return self.geocoder.get_coordinates(place_name, "finland")
            except LocationNotFound:
                return {"latitude": "", "longitude": ""}

        geocoordinates = get_coordinates_by_name(entry_name)

        village_coordinates = {"latitude": "", "longitude": ""}
        if village_name is not None:
            village_coordinates = get_coordinates_by_name(village_name)

        village_information = {
            KEYS["otherlocation"]: ValueWrapper(village_name or None),
            KEYS["othercoordinate"]: ValueWrapper({
                KEYS["latitude"]: village_coordinates["latitude"],
                KEYS["longitude"]: village_coordinates["longitude"]
            })
        }

        moved_in = ''
        moved_out = ''

        def add_location_to_list():
            self.location_listing.append(ValueWrapper({
                KEYS["otherlocation"]: ValueWrapper(entry_name),
                KEYS["othercoordinate"]: ValueWrapper({
                    KEYS["latitude"]: ValueWrapper(geocoordinates["latitude"]),
                    KEYS["longitude"]: ValueWrapper(geocoordinates["longitude"])
                }),
                KEYS["movedOut"]: ValueWrapper(moved_out),
                KEYS["movedIn"]: ValueWrapper(moved_in),
                KEYS["region"]: self.OTHER_REGION_ID,
                KEYS["village"]: ValueWrapper(village_information)
            }))

        if 'year_information' in location:
            for migration in location['year_information']:
                if 'moved_in' in migration:
                    moved_in = migration['moved_in']
                else:
                    moved_in = ''

                if 'moved_out' in migration:
                    moved_out = migration['moved_out']
                else:
                    moved_out = ''

                try:
                    if 41 <= int(moved_in) <= 43:
                        self.returned = True
                except ValueError:
                    pass

                add_location_to_list()
        else:
            add_location_to_list()

    def _constructReturnDict(self):
        loc = ValueWrapper(self.location_listing)
        loc.error = self.location_error
        return {KEYS["otherlocations"] : loc, KEYS["otherlocationsCount"] : ValueWrapper(len(self.location_listing))}


class LocationThresholdException(Exception):
    message = "Locations couldn't be found from db"

    def __unicode__(self):
        return repr(self.message)
