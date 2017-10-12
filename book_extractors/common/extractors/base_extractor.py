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
        self._dependee_results = None

        if options is not None and 'output_path' in options:
            self.output_path = options['output_path']
        else:
            self.output_path = None

        self.metadata_collector = MetadataCollector()

    def _get_data_at_parent_depth(self, results, depth):
        if depth > 0:
            results = results['parent_data']
            depth -= 1
            return self._get_data_at_parent_depth(results, depth)
        else:
            return results

    def _get_data_from_main_pipeline(self, results):
        if results['parent_data'] is None:
            return results
        else:
            results = results['parent_data']
            return self._get_data_from_main_pipeline(results)

    def _has_duplicates(self, extractor):
        return sum(this_tuple.count(extractor) for this_tuple in self._dependencies_graph) > 1

    def _resolve_dependencies(self):
        self._dependee_results = {}

        for dependee in self._dependencies_graph:
            extractor, context = dependee
            key = extractor.extraction_key

            extraction_results = {}

            if context == 'current':
                extraction_results = self._parent_pipeline_data['extraction_results']
            elif context == 'main':
                extraction_results = self._get_data_from_main_pipeline(self._parent_pipeline_data)['extraction_results']
            elif 'parent' in context:
                results_depth = context.count('parent')
                extraction_results = self._get_data_at_parent_depth(results_depth)
            else:
                raise SyntaxError('Something is wrong with your dependency contexts! The context has to be either'\
                                  'current, main or a string of however many parents you want.')

            result_key = key
            if self._has_duplicates(extractor):
                result_key = context + key

            self._dependee_results[result_key] = extraction_results[key]

    def extract(self, entry, extraction_results, extraction_metadata):
        if self._dependencies_graph is not None and self._dependencies_graph != []:
            self._resolve_dependencies()

        extraction_results, extraction_metadata = self._preprocess(entry, extraction_results, extraction_metadata)
        extraction_results, extraction_metadata = self._extract(entry, extraction_results, extraction_metadata)
        extraction_results, extraction_metadata = self._postprocess(entry, extraction_results, extraction_metadata)

        # Add finally the metadata after post process has been run since it might add metadata
        self._get_output_path(extraction_metadata)[self.extraction_key] = self.metadata_collector.get_metadata()
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
            return self._get_output_path(extraction_metadata)[self.key_of_cursor_location_dependent]['cursorLocation']
        else:
            return 0

    def get_last_cursor_location(self, extraction_results, extraction_metadata):
        cursor_locations_in_result_metadatas = [x['cursorLocation'] for x in extraction_metadata.values()]
        return max(cursor_locations_in_result_metadatas)

    def _get_output_path(self, root_collection):
        if self.output_path is None:
            return root_collection
        else:

            if self.output_path not in root_collection:
                root_collection[self.output_path] = {}

            return root_collection[self.output_path]    # TODO: Support arbitrary deep paths with syntax like "primaryPerson.extraStuff.importantStuff"

    def _add_to_extraction_results(self, data, extraction_results, extraction_metadata, cursor_location=0):
        self.metadata_collector.set_metadata_property('cursorLocation', cursor_location)
        self._get_output_path(extraction_results)[self.extraction_key] = data
        self._get_output_path(extraction_metadata)[self.extraction_key] = None  # This will be filled in by metadata collector

        return extraction_results, extraction_metadata
