# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from book_extractors.common.metadata_helper import MetadataCollector
from book_extractors.configuration_exceptions import DependencyConfigurationException
from book_extractors.configuration_exceptions import ContextKeywordConfigurationException
from book_extractors.configuration_exceptions import ParentKeywordConfigurationException
from book_extractors.extraction_exceptions import ParentKeywordTraversingException

class BaseExtractor:
    __metaclass__ = ABCMeta

    def __init__(self, cursor_location_depend_on=None, options=None, dependencies_contexts=None):

        if cursor_location_depend_on:
            self.key_of_cursor_location_dependent = cursor_location_depend_on.extraction_key # Tells key of entry in cursorLocations dict this extractor is dependent on
        else:
            self.key_of_cursor_location_dependent = None

        self.REQUIRES_MATCH_POSITION = False    # Set this to true in subclass if you want to enforce dependsOnMatchPositionOf() before extract()
        self.matchStartPosition = 0             # position in string where to begin match. Only used on certain classes
        self.matchFinalPosition = 0             # after extractor is finished, save the ending position of the match
        self._parent_pipeline_data = {}
        self._dependencies_graph = []
        self._required_dependencies = []
        self._deps = {}

        if options is not None and 'output_path' in options:
            self.output_path = options['output_path']
        else:
            self.output_path = None

        self.metadata_collector = MetadataCollector()

    def _build_dependencies_graph(self, dependencies_contexts):
        if dependencies_contexts:
            if len(dependencies_contexts) < len(self._required_dependencies):
                while len(dependencies_contexts) < len(self._required_dependencies):
                    dependencies_contexts.append(None)

                missing_contexts = []
                for ext, context in zip(self._required_dependencies, dependencies_contexts):
                    if context is None:
                        missing_contexts.append(ext.__name__)

                raise DependencyConfigurationException(missing_contexts)

            contexts = []
            for context in dependencies_contexts:
                new_context = context
                if isinstance(context, str):
                    new_context = (context, None)

                contexts.append(new_context)

            new_dependencies = [(extractor, context) for extractor, context in zip(self._required_dependencies, contexts)]
            self._dependencies_graph += new_dependencies

    def _set_dependencies(self, dependencies, dependencies_contexts):
        """
        When calling this function, contexts for every dependency need to be defined,
        including those that this extractor possibly inherits from its superclasses.
        The dependency and context lists must match each other positionally.

        Example: dependencies = [NameExtractor, SpouseExtractor]
                 contexts     = ['parent.parent', 'main']

        This tells the dependency system to look for MockExtractor's results in the
        parent pipeline of the parent pipeline, and for FoodExtractor's results in the
        main pipeline.

        When this function is called from a constructor that is called through super
        in a subclass, no contexts are passed. The superclass (and its superclasses)
        merely inserts its dependencies and is done. When this function is called
        through configure_extractor as it calls the extractor's constructor, the
        dependency graph is built as the contexts are passed into the constructor
        (and through that, here) through the extractor configuration.

        :param dependencies: A list of extractors (classes) whose results this extractor depends on.
        :param dependencies_contexts: A list of contexts for this extractor's dependencies. Contexts tell the dependency
        system where to find the dependencies. Valid keywords: 'current', 'main', 'parent', 'parent.parent.', ...
        :return:
        """
        for dependency in reversed(dependencies):
            self._required_dependencies.insert(0, dependency)

        if dependencies_contexts is not None:
            self._build_dependencies_graph(dependencies_contexts)

    def _get_data_from_parent_pipeline_results(self, results, parents_to_traverse):
        if parents_to_traverse > 0:
            if 'parent_data' not in results:
                raise ParentKeywordTraversingException()

            if results['parent_data'] is None:
                raise ParentKeywordConfigurationException()

            results = results['parent_data']
            parents_to_traverse -= 1
            return self._get_data_from_parent_pipeline_results(results, parents_to_traverse)
        else:
            return results

    def _get_data_from_main_pipeline(self, results):
        if results['parent_data'] is None:
            return results
        else:
            results = results['parent_data']
            return self._get_data_from_main_pipeline(results)

    def _has_duplicates(self, extractor):
        return sum(dependency_graph_tuple.count(extractor) for dependency_graph_tuple in self._dependencies_graph) > 1

    def _resolve_dependencies(self, current_extraction_results):
        self._deps = {}

        for dependency in self._dependencies_graph:
            extractor, context = dependency
            context, json_path = context
            key = extractor.extraction_key

            if context == 'current':
                extraction_results = current_extraction_results
            elif context == 'main':
                extraction_results = self._get_data_from_main_pipeline(self._parent_pipeline_data)['extraction_results']
            elif 'parent' in context:
                parents_to_traverse = context.count('parent') - 1
                extraction_results = self._get_data_from_parent_pipeline_results(self._parent_pipeline_data,
                                                                                 parents_to_traverse)['extraction_results']
            else:
                raise ContextKeywordConfigurationException()

            result_key = key
            if self._has_duplicates(extractor):
                result_key = context + '.' + key

            if json_path is not None:
                deps = extraction_results[json_path][key]
            else:
                deps = extraction_results[key]

            self._deps[result_key] = deps

    def _get_parent_data_for_pipeline(self, extraction_results, metadata):
        return {'extraction_results': extraction_results,
                'metadata': metadata,
                'parent_data': self._parent_pipeline_data}

    def extract(self, entry, extraction_results, extraction_metadata, parent_pipeline_data=None):
        self._parent_pipeline_data = parent_pipeline_data
        
        if self._dependencies_graph is not None and self._dependencies_graph != []:
            self._resolve_dependencies(extraction_results)

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
