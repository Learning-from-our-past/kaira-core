import pytest
from core.processdata import ProcessData
from core.pipeline_construction.dependency_resolver import ExtractorResultsMap
from core.tests.mock_xml_reader import MockXMLStreamer


def should_clear_result_map_after_extracting_one_entry():
    pipeline = MockPipeline()
    result_map = ExtractorResultsMap()
    process_data = ProcessData(pipeline, result_map)
    data = MockXMLStreamer([{'text': 'Person text'}])

    result_map.add_results('test', 'foo')
    assert result_map.get_results('test') == 'foo'

    results = process_data.run_extraction(data)

    assert len(results['entries']) == 1

    # After extraction, the map is empty and an exception is thrown
    with pytest.raises(Exception):
        result_map.get_results('test') == 'foo'


class MockPipeline:

    def process(self, entry):
        return {'data': entry}
