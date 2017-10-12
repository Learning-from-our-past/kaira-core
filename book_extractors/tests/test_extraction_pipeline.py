import pytest
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor

'''
TODO: Populate this file with many more tests for extraction_pipeline
'''

@pytest.mark.skip()
class TestExtractionPipelineDataPassing:
    def should_contain_parent_data_deep_in_the_subpipelines(self):
        test_pipeline = ExtractionPipeline([
            configure_extractor(MockExtractor),
            configure_extractor(MockExtractorAWithSubpipeline)
        ])
        parent_data = {
            'extraction_results': {
                'result': 'test'
            },
            'metadata': {
                'identity': 'i hate meta'
            },
            'parent_data': {
                'extraction_results': {
                    'name': {
                        'gender': 'Male'
                    },
                    'test_result': 'testiness',
                    'farmDetails': {
                        'farmTotalArea': 57.0
                    }
                },
                'metadata': {
                    'identity': 'i love meta'
                },
                'parent_data': None
            }
        }

        test_pipeline.process({'text': 'test string'}, parent_pipeline_data=parent_data)
        '''
        The assert for this test happens in the _extract function of the MockExtractorDeepPipelineTest class.
        CTRL + F to "parent_results_deep assert here" to get there.
        '''


class MockExtractorDeepPipelineTest(BaseExtractor):
    extraction_key = 'mock'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(MockExtractorDeepPipelineTest, self).__init__(key_of_cursor_location_dependent, options)

    def _extract(self, entry, extraction_results, extraction_metadata):
        correct_results = {
            'extraction_results': {
                'name': {
                    'gender': 'Male'
                },
                'test_result': 'testiness',
                'farmDetails': {
                    'farmTotalArea': 57.0
                }
            },
            'metadata': {
                'identity': 'i love meta'
            },
            'parent_data': None
        }

        '''
        First parent refers to MockExtractorBWithSubpipeline, whose parent refers to MockExtractorAWithSubpipeline,
        whose parent refers to the main pipeline in this test, built in the should function.
        '''
        assert_results = self._parent_pipeline_data['parent_data']['parent_data']['parent_data']

        # parent_results_deep assert here
        assert assert_results == correct_results

        return self._add_to_extraction_results('mock result', extraction_results, extraction_metadata)


class MockExtractor(BaseExtractor):
    extraction_key = 'mock'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(MockExtractor, self).__init__(key_of_cursor_location_dependent, options)

    def _extract(self, entry, extraction_results, extraction_metadata):
        return self._add_to_extraction_results('mock result', extraction_results, extraction_metadata)


class MockExtractorAWithSubpipeline(BaseExtractor):
    extraction_key = 'mock_a_with_sub'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(MockExtractorAWithSubpipeline, self).__init__(key_of_cursor_location_dependent, options)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(MockExtractor),
            configure_extractor(MockExtractorBWithSubpipeline)
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        parent_data = {'extraction_results': extraction_results, 'parent_data': self._parent_pipeline_data}
        results, metadata = self._sub_extraction_pipeline.process(entry, parent_pipeline_data=parent_data)

        return self._add_to_extraction_results(results, extraction_results, extraction_metadata)


class MockExtractorBWithSubpipeline(BaseExtractor):
    extraction_key = 'mock_b_with_sub'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(MockExtractorBWithSubpipeline, self).__init__(key_of_cursor_location_dependent, options)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(MockExtractor),
            configure_extractor(MockExtractorDeepPipelineTest)
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        parent_data = {'extraction_results': extraction_results, 'parent_data': self._parent_pipeline_data}
        results, metadata = self._sub_extraction_pipeline.process(entry, parent_pipeline_data=parent_data)

        return self._add_to_extraction_results(results, extraction_results, extraction_metadata)
