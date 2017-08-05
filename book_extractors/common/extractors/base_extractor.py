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

    def extract(self, entry, extraction_results, extraction_metadata):
        extraction_results, extraction_metadata = self._preprocess(entry, extraction_results, extraction_metadata)
        extraction_results, extraction_metadata = self._extract(entry, extraction_results, extraction_metadata)
        extraction_results, extraction_metadata = self._postprocess(entry, extraction_results, extraction_metadata)

        # Add finally the metadata after post process has been run since it might add metadata
        extraction_metadata[self.extraction_key] = self.metadata_collector.get_metadata()
        self.metadata_collector.clear()

        return extraction_results, extraction_metadata

    def _preprocess(self, entry, extraction_results, extraction_metadata):
        """
        Optional implementable method for child classes. Run before _extract method. 
        Lets to manipulate input data for extraction logic.
        :param entry: 
        :param extraction_results: 
        :return extraction_results:
        """
        return extraction_results, extraction_metadata

    @abstractmethod
    def _extract(self, entry, extraction_results, extraction_metadata):
        """
        Required method for child classes. Should contain main data extraction logic.
        :param entry: 
        :param extraction_results: 
        :return extraction_results: 
        """
        pass

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        """
        Optional implementable method for child classes. Run after _extract method.
        Lets to manipulate results of the extractor.
        :param entry: 
        :param extraction_results: 
        :return extraction_results:
        """
        return extraction_results, extraction_metadata

    def get_starting_position(self, extraction_results, extraction_metadata):
        if self.key_of_cursor_location_dependent is not None:
            return extraction_metadata[self.key_of_cursor_location_dependent]['cursorLocation']
        else:
            return 0

    def get_last_cursor_location(self, extraction_results, extraction_metadata):
        cursor_locations_in_result_metadatas = [x['cursorLocation'] for x in extraction_metadata.values()]
        return max(cursor_locations_in_result_metadatas)

    def _add_to_extraction_results(self, data, extraction_results, extraction_metadata, cursor_location=0):
        self.metadata_collector.set_metadata_property('cursorLocation', cursor_location)
        extraction_results[self.extraction_key] = data
        extraction_metadata[self.extraction_key] = None  # This will be filled in by metadata collector

        return extraction_results, extraction_metadata
