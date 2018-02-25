# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from book_extractors.common.metadata_helper import MetadataCollector
from core.configuration_exceptions import RequiredDependenciesAreMissing
from core.extraction_pipeline import ExtractionPipeline


class BaseExtractor:
    __metaclass__ = ABCMeta

    def __init__(self, cursor_location_depends_on=None, options=None):

        if cursor_location_depends_on:
            # Tells key of entry in cursorLocations dict this extractor is dependent on
            self.key_of_cursor_location_dependent = cursor_location_depends_on.extraction_key
        else:
            self.key_of_cursor_location_dependent = None

        self._sub_extraction_pipeline = None
        self._extraction_results_map = None

        self._expected_dependencies_names = []
        self._required_dependencies = []
        self._deps = {}

        if options is not None and 'output_path' in options:
            self.output_path = options['output_path']
        else:
            self.output_path = None

        self.metadata_collector = MetadataCollector()

    def set_subpipeline(self, extractors):
        """
        Defines the sub pipeline for the extractor. Called during YAML-parsing process.
        :param extractors:
        :return:
        """
        self._sub_extraction_pipeline = ExtractionPipeline(extractors)

    def set_extraction_results_map(self, results_map):
        """
        Pass the result map to extractor. It contains the pure unmodified extraction results of the previous
        extractors in a map which can be used to resolve those results as a dependencies to this extractor.
        :param results_map:
        :return:
        """
        self._extraction_results_map = results_map

    def _declare_expected_dependency_names(self, dependency_names):
        """
        If extractor has dependencies, declare their names here in constructor. The provided names
        are just names which can later be used to fetch resolved results during extraction. However, the amount
        of the names is verified when required dependencies are set, so that no less nor no more dependencies
        are injected to the extractor than is expected.
        The names should be defined in the same order as dependencies are listed in the yaml-configuration.
        :param dependency_names: list of strings
        :return:
        """
        self._expected_dependencies_names = dependency_names

    def set_required_dependencies(self, extractor_dependencies):
        """
        Set possible required dependencies based on YAML config. A list of extractors or their ids/names so that the
        dependencies can be resolved from the extraction_results_map during the extraction.

        Usually one should provide extractor objects like YamlParser does when config-file uses PyYaml anchors. However,
        it is also possible to just pass a strings which will then act as keys in the extraction results map instead
        of object ids. This is recommended approach when mocking dependencies in unit tests.

        :param extractor_dependencies: Extractor object or string.
        :return:
        """

        def map_dependencies(dep):
            if type(dep) is str:
                return dep
            else:
                return id(dep)

        self._required_dependencies = list(map(map_dependencies, extractor_dependencies))

        if len(self._required_dependencies) != len(self._expected_dependencies_names):
            raise RequiredDependenciesAreMissing()

    def _resolve_dependencies(self):

        result_data = [self._extraction_results_map.get_results(dep_id) for dep_id in self._required_dependencies]

        self._deps = {key: data for (key, data) in zip(self._expected_dependencies_names, result_data)}

    def extract(self, entry, extraction_results, extraction_metadata):
        self._resolve_dependencies()

        extraction_results, extraction_metadata = self._preprocess(entry, extraction_results, extraction_metadata)
        extraction_results, extraction_metadata = self._extract(entry, extraction_results, extraction_metadata)
        extraction_results, extraction_metadata = self._postprocess(entry, extraction_results, extraction_metadata)

        # Add finally the metadata after post process has been run since it might add metadata
        self._get_output_path(extraction_metadata)[self.extraction_key] = self.metadata_collector.get_metadata()
        self.metadata_collector.clear()

        # Store this extractor's results to the map so that it can be used later for dependency resolving
        # Strip the output path, since we don't want to store it to the result map
        extraction_results_without_output_path = extraction_results
        if self.output_path:
            extraction_results_without_output_path = extraction_results[self.output_path]
        self._extraction_results_map.add_results(id(self), extraction_results_without_output_path)

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

    def get_starting_position(self, extraction_metadata):
        if self.key_of_cursor_location_dependent is not None:
            return self._get_output_path(extraction_metadata)[self.key_of_cursor_location_dependent]['cursorLocation']
        else:
            return 0

    def get_last_cursor_location(self, extraction_metadata):
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
