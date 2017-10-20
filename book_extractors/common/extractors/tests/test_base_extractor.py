import pytest
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.configuration_exceptions import DependencyConfigurationException, ParentKeywordConfigurationException
from book_extractors.configuration_exceptions import ContextKeywordConfigurationException
from book_extractors.extraction_exceptions import ParentKeywordTraversingException


class TestBaseExtractor:

    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return MockExtractor()

    class TestPreprocess:
        def should_run_preprocess_and_post_process_if_implemented(self, extractor):
            entry = {'text': 'test string entry'}
            results, metadata = extractor.extract(entry, {}, {})
            assert extractor.execution_order == ['preprocess', 'extract', 'postprocess']
            assert results['mock'] == 'SOME RESULT'

        def should_not_run_preprocess_and_post_process_if_they_are_not_implemented(self):
            extractor = NoPreAndPostProcessesExtractor()
            entry = {'text': 'test string entry'}
            results, metadata = extractor.extract(entry, {}, {})
            assert extractor.execution_order == ['extract']
            assert results['mock2'] == 'some result'

    class TestDependencies:
        def should_correctly_set_up_a_dependency_and_its_context_in_extractor(self):
            dep_context = 'parent'

            parent_data = {'extraction_results': {MockExtractor.extraction_key: 'test'}}
            my_pipeline = ExtractionPipeline([
                configure_extractor(SimpleExtractorForDeps, dependencies_contexts=[dep_context]),
            ])

            results, metadata = my_pipeline.process({'text': 'test string'}, parent_pipeline_data=parent_data)
            extractor_dependencies_graph = metadata[SimpleExtractorForDeps.extraction_key]['dependencies_graph'][0]
            correct_dependencies_graph = (MockExtractor, (dep_context, None))
            assert extractor_dependencies_graph == correct_dependencies_graph

        def should_correctly_set_up_multiple_dependencies_and_contexts_in_extractor(self):
            my_pipeline = ExtractionPipeline([
                configure_extractor(SimpleExtractorForMultiDeps, dependencies_contexts=['parent', 'main', 'main'])
            ])

            parent_data = {'extraction_results': {MockExtractor.extraction_key: 'test'},
                           'parent_data': {
                               'extraction_results': {NoPreAndPostProcessesExtractor.extraction_key: 'test',
                                                      SimpleExtractorForDeps.extraction_key: 'test'},
                               'parent_data': None
                           }}

            results, metadata = my_pipeline.process({'text': 'test string'}, parent_pipeline_data=parent_data)
            extractor_dependencies_graph = metadata[SimpleExtractorForMultiDeps.extraction_key]['dependencies_graph']
            correct_dependencies_graph = [
                (MockExtractor, ('parent', None)),
                (NoPreAndPostProcessesExtractor, ('main', None)),
                (SimpleExtractorForDeps, ('main', None))
            ]

            assert extractor_dependencies_graph == correct_dependencies_graph

        def should_raise_dependency_configuration_error_if_the_number_of_dependencies_and_contexts_does_not_match(self):
            with pytest.raises(DependencyConfigurationException) as excinfo:
                my_pipeline = ExtractionPipeline([
                    configure_extractor(SimpleExtractorForMultiDeps, dependencies_contexts=['main'])
                ])

            assert excinfo.value.missing_contexts == [NoPreAndPostProcessesExtractor.__name__,
                                                      SimpleExtractorForDeps.__name__]

        def should_raise_parent_context_configuration_error_if_there_are_too_many_parents_in_contexts(self):
            my_pipeline = ExtractionPipeline([
                configure_extractor(SimpleExtractorForDeps, dependencies_contexts=['parent.parent'])
            ])

            parent_data = {'extraction_results': {'test': 'test'},
                           'parent_data': None}

            with pytest.raises(ParentKeywordConfigurationException):
                my_pipeline.process({'text': 'test'}, parent_pipeline_data=parent_data)

        def should_raise_parent_traversing_error_if_parent_data_is_missing_from_parent_pipeline_data_during_any_traverse_step(self):
            my_pipeline = ExtractionPipeline([
                configure_extractor(SimpleExtractorForDeps, dependencies_contexts=['parent.parent'])
            ])

            parent_data = {'extraction_results': {'test': 'test'}}

            with pytest.raises(ParentKeywordTraversingException):
                my_pipeline.process({'text': 'test'}, parent_pipeline_data=parent_data)

        def should_raise_context_keyword_configuration_error_if_context_is_entered_in_an_unrecognized_way(self):
            my_pipeline = ExtractionPipeline([
                configure_extractor(SimpleExtractorForDeps, dependencies_contexts=['sfdjhö'])
            ])

            with pytest.raises(ContextKeywordConfigurationException):
                my_pipeline.process({'text': 'test'})

    class TestMetadata:
        def should_reset_metadata_collector_after_extraction(self, extractor):
            entry = {'text': 'test string entry'}

            assert extractor.metadata_collector.get_metadata() == {'errors': {}}

            results, metadata = extractor.extract(entry, {}, {})

            assert metadata['mock']['important'] is True
            assert extractor.metadata_collector.get_metadata() == {'errors': {}} # Collector should be empty again

        def should_provide_starting_position_and_get_previous_cursor_location_correctly_when_required(self):
            extractor = MockExtractor('previousExtractor')
            entry = {'text': 'test string entry'}
            extraction_results = {
                'previousExtractor': {
                    'results': 'something',
                }
            }

            metadata = {
                'previousExtractor': {
                    'cursorLocation': 10
                }
            }

            results, metadata = extractor.extract(entry, extraction_results, metadata)
            assert metadata['mock']['cursorLocation'] == 15  # Starting position + end position

    def should_set_starting_position_0_when_it_is_not_required(self, extractor):
        entry = {'text': 'test string entry'}
        results, metadata = extractor.extract(entry, {}, {})

        last_position = extractor.get_last_cursor_location(results, metadata)
        assert last_position == 5

    def should_add_results_with_metadata_to_data_passed_in(self, extractor):
        entry = {'text': 'test string entry'}
        results, metadata = extractor.extract(entry, {}, {})

        assert results['mock'] is not None
        assert results['mock'] == 'SOME RESULT'
        assert metadata['mock'] is not None
        assert metadata['mock']['important'] is True
        assert metadata['mock']['cursorLocation'] == 5
        assert metadata['mock']['errors'] == {}

    class TestPassingParentData:
        def should_correctly_set_parent_data_in_extractor(self, extractor):
            entry = {'text': 'test string entry'}
            correct_data = {'test_data': 'i am test, awooooo'}
            results, metadata = extractor.extract(entry, {}, {}, parent_pipeline_data=correct_data)
            parent_data = metadata[extractor.extraction_key]['parent_pipeline_data']

            assert parent_data == correct_data


class MockExtractor(BaseExtractor):
    extraction_key = 'mock'

    def __init__(self, key_of_cursor_location_dependent=None, options=None):
        super(MockExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.execution_order = []

    def _preprocess(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('preprocess')
        return extraction_results, extraction_metadata

    def _extract(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('extract')
        self.metadata_collector.set_metadata_property('important', True)

        final_location = self.get_starting_position(extraction_results, extraction_metadata) + 5

        self.metadata_collector.set_metadata_property('parent_pipeline_data', self._parent_pipeline_data)

        return self._add_to_extraction_results('some result', extraction_results,
                                               extraction_metadata, cursor_location=final_location)

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('postprocess')
        extraction_results[self.extraction_key] = extraction_results[self.extraction_key].upper()
        return extraction_results, extraction_metadata


class NoPreAndPostProcessesExtractor(BaseExtractor):
    extraction_key = 'mock2'

    def __init__(self, key_of_cursor_location_dependent=None, options=None):
        super(NoPreAndPostProcessesExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.execution_order = []

    def _extract(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('extract')
        self.metadata_collector.set_metadata_property('important', True)

        final_location = self.get_starting_position(extraction_results, extraction_metadata) + 5

        return self._add_to_extraction_results('some result', extraction_results,
                                               extraction_metadata, cursor_location=final_location)


class SimpleExtractorForDeps(BaseExtractor):
    extraction_key = 'mock2deps'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(SimpleExtractorForDeps, self).__init__(key_of_cursor_location_dependent,
                                                     options)

        my_dependencies = [MockExtractor]
        self._set_dependencies(my_dependencies, dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        self.metadata_collector.set_metadata_property('dependencies_graph', self._dependencies_graph)

        return self._add_to_extraction_results('some result', extraction_results, extraction_metadata)


class SimpleExtractorForMultiDeps(BaseExtractor):
    extraction_key = 'mock2multideps'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(SimpleExtractorForMultiDeps, self).__init__(key_of_cursor_location_dependent,
                                                          options)

        my_dependencies = [MockExtractor, NoPreAndPostProcessesExtractor, SimpleExtractorForDeps]
        self._set_dependencies(my_dependencies, dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        self.metadata_collector.set_metadata_property('dependencies_graph', self._dependencies_graph)

        return self._add_to_extraction_results('some result', extraction_results, extraction_metadata)
