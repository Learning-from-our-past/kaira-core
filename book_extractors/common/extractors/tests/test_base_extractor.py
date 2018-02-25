import pytest
from book_extractors.common.extractors.base_extractor import BaseExtractor
from pipeline.configuration_exceptions import RequiredDependenciesAreMissing
from pipeline.extraction_pipeline import ExtractionPipeline
from pipeline.dependency_resolver import ExtractorResultsMap


class TestBaseExtractor:

    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        extractor = MockExtractor()
        extractor.set_extraction_results_map(ExtractorResultsMap())
        return extractor

    class TestPreprocess:
        def should_run_preprocess_and_post_process_if_implemented(self, extractor):
            entry = {'text': 'test string entry'}
            results, metadata = extractor.extract(entry, {}, {})
            assert extractor.execution_order == ['preprocess', 'extract', 'postprocess']
            assert results['mock'] == 'SOME RESULT'

        def should_not_run_preprocess_and_post_process_if_they_are_not_implemented(self, th):
            extractor = th.setup_extractor(NoPreAndPostProcessesExtractor())
            entry = {'text': 'test string entry'}
            results, metadata = extractor.extract(entry, {}, {})
            assert extractor.execution_order == ['extract']
            assert results['mock2'] == 'some result'

    class TestMetadata:
        def should_reset_metadata_collector_after_extraction(self, extractor):
            entry = {'text': 'test string entry'}

            assert extractor.metadata_collector.get_metadata() == {'errors': {}}

            results, metadata = extractor.extract(entry, {}, {})

            assert metadata['mock']['important'] is True
            assert extractor.metadata_collector.get_metadata() == {'errors': {}} # Collector should be empty again

        def should_provide_starting_position_and_get_previous_cursor_location_correctly_when_required(self, th):
            extractor = th.setup_extractor(MockExtractor(NoPreAndPostProcessesExtractor))
            entry = {'text': 'test string entry'}
            extraction_results = {
                'mock2': {
                    'results': 'something',
                }
            }

            metadata = {
                'mock2': {
                    'cursorLocation': 10
                }
            }

            results, metadata = extractor.extract(entry, extraction_results, metadata)
            assert metadata['mock']['cursorLocation'] == 15  # Starting position + end position

    def should_set_starting_position_0_when_it_is_not_required(self, extractor):
        entry = {'text': 'test string entry'}
        results, metadata = extractor.extract(entry, {}, {})

        last_position = extractor.get_last_cursor_location(metadata)
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

    class TestDependencyResolving:

        @pytest.fixture()
        def result_map(self):
            return ExtractorResultsMap()

        @pytest.fixture()
        def dep_extractors(self, result_map):
            """
            Set two extractors where the second one depends on first.
            """
            extractor1 = MockExtractor()
            extractor2 = MockExtractor()
            extractor1.set_extraction_results_map(result_map)
            extractor2.set_extraction_results_map(result_map)

            dependent_extractor = SimpleExtractorForDeps()
            dependent_extractor.set_extraction_results_map(result_map)

            dependent_extractor.set_required_dependencies([extractor1, extractor2])

            return {'standalone': [extractor1, extractor2], 'dependent': dependent_extractor}

        def should_set_ids_of_required_extractors(self, dep_extractors):
            # Extractor should hold the id of the extractor1 which will be used for resolving
            assert dep_extractors['dependent']._required_dependencies == [id(dep_extractors['standalone'][0]),
                                                                          id(dep_extractors['standalone'][1])]

        def should_assign_dependency_names_to_a_corresponding_dependencies(self, dep_extractors):
            # The declared names and the order of set dependencies should be the same
            assert dep_extractors['dependent']._required_dependencies == [id(dep_extractors['standalone'][0]),
                                                                          id(dep_extractors['standalone'][1])]
            assert dep_extractors['dependent']._expected_dependencies_names == ['standalone', 'standalone2']

        def should_resolve_dependencies_to_deps_object_before_extraction(self, dep_extractors):
            extractors = [dep_extractors['standalone'][0], dep_extractors['standalone'][1], dep_extractors['dependent']]
            pipeline = ExtractionPipeline(extractors)
            results = pipeline.process({'text': 'test string'})

            # The result of the standalone extractor should be available in latter extractor
            assert dep_extractors['dependent']._deps == {'standalone': {'mock': 'SOME RESULT'},
                                                         'standalone2': {'mock': 'SOME RESULT'}}
            # And it should have been used to generate the results
            assert results[0]['mock2deps'] == 'This is from standalone extractor: SOME RESULT'

        def should_store_extraction_results_to_the_extraction_results_map(self, result_map, dep_extractors):
            extractors = [dep_extractors['standalone'][0], dep_extractors['standalone'][1], dep_extractors['dependent']]
            pipeline = ExtractionPipeline(extractors)
            pipeline.process({'text': 'test string'})

            assert result_map.get_results(id(dep_extractors['standalone'][0])) == {'mock': 'SOME RESULT'}
            assert result_map.get_results(id(dep_extractors['standalone'][1])) == {'mock': 'SOME RESULT'}

        def should_raise_error_if_incorrect_amount_of_dependencies_were_provided(self, result_map):
            extractor1 = MockExtractor()
            extractor1.set_extraction_results_map(result_map)

            dependent_extractor = SimpleExtractorForDeps()
            dependent_extractor.set_extraction_results_map(result_map)

            with pytest.raises(RequiredDependenciesAreMissing):
                dependent_extractor.set_required_dependencies([extractor1, extractor1, extractor1])

        @pytest.mark.skip()
        def should_raise_resolving_error_if_dependency_could_not_be_resolved(self):
            pass


class MockExtractor(BaseExtractor):
    extraction_key = 'mock'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(MockExtractor, self).__init__(cursor_location_depends_on, options)
        self.execution_order = []

    def _preprocess(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('preprocess')
        return extraction_results, extraction_metadata

    def _extract(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('extract')
        self.metadata_collector.set_metadata_property('important', True)

        final_location = self.get_starting_position(extraction_metadata) + 5

        return self._add_to_extraction_results('some result', extraction_results,
                                               extraction_metadata, cursor_location=final_location)

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('postprocess')
        extraction_results[self.extraction_key] = extraction_results[self.extraction_key].upper()
        return extraction_results, extraction_metadata


class NoPreAndPostProcessesExtractor(BaseExtractor):
    extraction_key = 'mock2'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(NoPreAndPostProcessesExtractor, self).__init__(cursor_location_depends_on, options)
        self.execution_order = []

    def _extract(self, entry, extraction_results, extraction_metadata):
        self.execution_order.append('extract')
        self.metadata_collector.set_metadata_property('important', True)

        final_location = self.get_starting_position(extraction_metadata) + 5

        return self._add_to_extraction_results('some result', extraction_results,
                                               extraction_metadata, cursor_location=final_location)


class SimpleExtractorForDeps(BaseExtractor):
    extraction_key = 'mock2deps'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(SimpleExtractorForDeps, self).__init__(cursor_location_depends_on, options)

        self._declare_expected_dependency_names(['standalone', 'standalone2'])

    def _extract(self, entry, extraction_results, extraction_metadata):
        result = 'This is from standalone extractor: {}'.format(self._deps['standalone']['mock'])
        return self._add_to_extraction_results(result, extraction_results, extraction_metadata)
