# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class BaseExtractor():
    __metaclass__ = ABCMeta

    def __init__(self, key_of_cursor_location_dependent=None, options=None):
        self.key_of_cursor_location_dependent = key_of_cursor_location_dependent    # Tells key of entry in cursorLocations dict this extractor is dependent on
        self.REQUIRES_MATCH_POSITION = False    # Set this to true in subclass if you want to enforce dependsOnMatchPositionOf() before extract()
        self.matchStartPosition = 0             # position in string where to begin match. Only used on certain classes
        self.matchFinalPosition = 0             # after extractor is finished, save the ending position of the match

    @abstractmethod
    def extract(self, entry, extraction_results):
        self._checkIfMatchPositionIsRequiredBeforeExtract()

    def getFinalMatchPosition(self):
        return self.matchFinalPosition

    def get_starting_position(self, extraction_results):
        if self.key_of_cursor_location_dependent is not None:
            return extraction_results['cursor_locations'][self.key_of_cursor_location_dependent]
        else:
            return 0

    def get_last_cursor_location(self, extraction_results):
        return max(extraction_results['cursor_locations'].values())

    def _constructReturnDict(self, data, extraction_results, cursor_location=0):
        extraction_results['data'] = {**data, **extraction_results['data']}
        extraction_results['cursor_locations'][self.__class__.__name__] = cursor_location
        return extraction_results

    def _checkIfMatchPositionIsRequiredBeforeExtract(self):
        if self.REQUIRES_MATCH_POSITION and self.matchStartPosition == -1:
            raise MatchPositionRequiredException()


class MatchPositionRequiredException(Exception):
    message = u"Match position required to supplied with dependsOnMatchPositionOf before extract call. "

    def __init__(self, details = ""):
        self.message += details

    def __unicode__(self):
        return self.message
