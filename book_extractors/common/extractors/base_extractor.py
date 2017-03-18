# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from book_extractors.common.metadata_helper import MetadataCollector


class BaseExtractor:
    __metaclass__ = ABCMeta

    def __init__(self, key_of_cursor_location_dependent=None, options=None):
        self.key_of_cursor_location_dependent = key_of_cursor_location_dependent    # Tells key of entry in cursorLocations dict this extractor is dependent on
        self.REQUIRES_MATCH_POSITION = False    # Set this to true in subclass if you want to enforce dependsOnMatchPositionOf() before extract()
        self.matchStartPosition = 0             # position in string where to begin match. Only used on certain classes
        self.matchFinalPosition = 0             # after extractor is finished, save the ending position of the match
        self.metadata_collector = MetadataCollector()

    @abstractmethod
    def extract(self, entry, extraction_results):
        self._checkIfMatchPositionIsRequiredBeforeExtract()

    def get_starting_position(self, extraction_results):
        if self.key_of_cursor_location_dependent is not None:
            return extraction_results[self.key_of_cursor_location_dependent]['metadata']['cursorLocation']
        else:
            return 0

    def get_last_cursor_location(self, extraction_results):
        # TODO: Eli kaikkien dictin avainten metadataobjektin cursorLocation results
        cursor_locations_in_result_metadatas = [x['metadata']['cursorLocation'] for x in extraction_results.values()]

        return max(cursor_locations_in_result_metadatas)

    def _constructReturnDict(self, data, extraction_results, cursor_location=0):
        self.metadata_collector.set_metadata_property('cursorLocation', cursor_location)
        extraction_results[self.extraction_key] = {
            'results': data,
            'metadata': self.metadata_collector.get_metadata()
        }

        self.metadata_collector.clear()
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
