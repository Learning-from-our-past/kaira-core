import pytest
from book_extractors.common.extractors.base_extractor import BaseExtractor


class TestBaseExtractor:

    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return MockExtractor()

    class TestPreprocess:
        def should_run_preprocess_and_post_process_if_implemented(self, extractor):
            entry = {'text': 'test string entry'}
            extraction_results = {}
            results = extractor.extract(entry, extraction_results)
            assert extractor.execution_order == ['preprocess', 'extract', 'postprocess']
            assert results['mock']['results'] == 'SOME RESULT'

        def should_not_run_preprocess_and_post_process_if_they_are_not_implemented(self):
            extractor = NoPreAndPostProcessesExtractor()
            entry = {'text': 'test string entry'}
            extraction_results = {}
            results = extractor.extract(entry, extraction_results)
            assert extractor.execution_order == ['extract']
            assert results['mock2']['results'] == 'some result'

    class TestMetadata:
        def should_reset_metadata_collector_after_extraction(self, extractor):
            entry = {'text': 'test string entry'}
            extraction_results = {}

            assert extractor.metadata_collector.get_metadata() == {'errors': {}}

            results = extractor.extract(entry, extraction_results)

            assert results['mock']['metadata']['important'] is True
            assert extractor.metadata_collector.get_metadata() == {'errors': {}} # Collector should be empty again

        def should_provide_starting_position_and_get_previous_cursor_location_correctly_when_required(self):
            extractor = MockExtractor('previousExtractor')
            entry = {'text': 'test string entry'}
            extraction_results = {
                'previousExtractor': {
                    'results': 'something',
                    'metadata': {
                        'cursorLocation': 10
                    }
                }
            }

            results = extractor.extract(entry, extraction_results)
            assert results['mock']['metadata']['cursorLocation'] == 15  # Starting position + end position

    def should_set_starting_position_0_when_it_is_not_required(self, extractor):
        entry = {'text': 'test string entry'}
        extraction_results = {}
        results = extractor.extract(entry, extraction_results)

        last_position = extractor.get_last_cursor_location(results)
        assert last_position == 5

    def should_add_results_with_metadata_to_data_passed_in(self, extractor):
        entry = {'text': 'test string entry'}
        extraction_results = {}
        results = extractor.extract(entry, extraction_results)

        assert results['mock'] is not None
        assert results['mock']['results'] == 'SOME RESULT'
        assert results['mock']['metadata'] is not None
        assert results['mock']['metadata']['important'] is True
        assert results['mock']['metadata']['cursorLocation'] == 5
        assert results['mock']['metadata']['errors'] == {}


class MockExtractor(BaseExtractor):
    extraction_key = 'mock'

    def __init__(self, key_of_cursor_location_dependent=None, options=None):
        super(MockExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.execution_order = []

    def _preprocess(self, entry, extraction_results):
        self.execution_order.append('preprocess')
        return extraction_results

    def _extract(self, entry, extraction_results):
        self.execution_order.append('extract')
        self.metadata_collector.set_metadata_property('important', True)

        final_location = self.get_starting_position(extraction_results) + 5

        return self._add_to_extraction_results('some result', extraction_results, cursor_location=final_location)

    def _postprocess(self, entry, extraction_results):
        self.execution_order.append('postprocess')
        extraction_results[self.extraction_key]['results'] = extraction_results[self.extraction_key]['results'].upper()
        return extraction_results


class NoPreAndPostProcessesExtractor(BaseExtractor):
    extraction_key = 'mock2'

    def __init__(self, key_of_cursor_location_dependent=None, options=None):
        super(NoPreAndPostProcessesExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.execution_order = []

    def _extract(self, entry, extraction_results):
        self.execution_order.append('extract')
        self.metadata_collector.set_metadata_property('important', True)

        final_location = self.get_starting_position(extraction_results) + 5

        return self._add_to_extraction_results('some result', extraction_results, cursor_location=final_location)