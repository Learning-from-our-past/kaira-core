import regex
import core.utils.regex_utils as regexUtils
from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils import text_utils
from core.utils.geo.geocoding import GeoCoder, LocationNotFound
from core.utils.text_utils import remove_hyphens_from_text
from extractors.common.postprocessors import place_name_cleaner


class BirthLocationExtractor(BaseExtractor):
    extraction_key = 'birthLocation'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super().__init__(cursor_location_depends_on, options)
        self._SUBSTRING_WIDTH = 32
        self._PATTERN = r'\d\s(?P<placeName>[\w-]+(?:\smlk)?)(?:[,.])'
        self._OPTIONS = (regex.UNICODE | regex.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)

        location_entry, cursor_location = self._get_location_data(prepared_text, start_position)
        return self._add_to_extraction_results(location_entry, extraction_results, extraction_metadata, cursor_location)

    def _prepare_text_for_extraction(self, text, start_position):
        return text_utils.take_sub_str_based_on_pos(text, start_position, self._SUBSTRING_WIDTH)

    def _get_location_data(self, text, start_position):
        place_name, cursor_location = self._find_place_name(text, start_position)
        if place_name is not None:
            place_name = self._clean_place_name(place_name)
            location_entry = self._augment_location_data(place_name)
        else:
            location_entry = None

        return location_entry, cursor_location

    def _find_place_name(self, text, start_position):
        # FIXME: This is kinda desperate way to pick the birth location string. The start position is off since looks like our
        # birth location extractor does not set its cursor location properly to the end of its match. This means we have
        # to deal here with dates being in the substring's beginning... We should probably fix the CommonBirthDayExtractor to
        # set its location correctly at some point.
        try:
            match = regexUtils.safe_search(self._PATTERN, text, self._OPTIONS)
            return match.group('placeName'), start_position + match.end()
        except regexUtils.RegexNoneMatchException:
            return None, start_position

    def _clean_place_name(self, place_name):
        place_name = remove_hyphens_from_text(place_name)
        place_name = place_name.replace('\s', '')
        return place_name

    def _augment_location_data(self, place_name):
        location_entry = {
            'locationName': place_name,
            'latitude': None,
            'longitude': None
        }

        location_entry = place_name_cleaner.clean_place_name(location_entry)
        location_entry = place_name_cleaner.normalize_place(location_entry)

        # Try to find coordinates and region of the place from our geo database
        # If coordinates were found, merge them to the location entry dict.
        try:
            region_and_coordinates = GeoCoder.get_coordinates(location_entry['locationName'])
            location_entry = {**location_entry, **region_and_coordinates}
        except LocationNotFound:
            pass

        return location_entry
