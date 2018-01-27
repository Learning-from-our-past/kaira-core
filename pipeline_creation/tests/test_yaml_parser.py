import pytest

from book_extractors.common.extractors.base_extractor import BaseExtractor
from pipeline_creation.yaml_parser import parse_config, build_pipeline_from_yaml
from book_extractors.karelians.extraction.extractors.name_extractor import NameExtractor

test_data = {
    'name': 'TESTINEN. VÄINÖ',
    'text': 'maanviljelijä, synt. 26. 1. -27 Testilässä. Puol. Vaimo Vaimonen o.s. Vaimoke, emäntä, synt. 7 7. -32 '
            'Enossa. Avioit. -51. Lapset: Martti Olavi An tero -51, Martta Lyyli 53, Mikko Timo Tapani -55, Matti '
            'Armas Juhani -57. Merja Riitta Sinikka -59, Marjatta Raija Orvokki -63. Syntyneet Enossa Asuinp. '
            'Karjalassa: Ruskeala, Kaalamo 27—40, 40—44 Muut asuinp.: Svsmä, Rapola -40 Isokyrö. Lehmijoki 41—45, '
            'Kiihtelysvaara 45—48, Eno, Haapalahti 48—. Testiset asuvat maatilalla, jonka pinta-ala on 15,5 ha, '
            'viljeltyä on 5.7 ha. Maanviljelyksen ohella harjoitetaan karjanhoitoa.'
}


def should_load_yaml():
    result = parse_config('pipeline_creation/tests/test_config.yaml')
    assert result['book_series'] == 'Siirtokarjalaisten tie'
    assert len(result['pipeline']) == 14
    assert type(result['pipeline'][0]) is NameExtractor


def should_build_and_run_pipeline():
    pipeline = build_pipeline_from_yaml('pipeline_creation/tests/test_config.yaml')

    results = pipeline.process(test_data)

    assert results[0]['primaryPerson']['name']['surname'] == 'TESTINEN'
    assert results[0]['primaryPerson']['profession']['professionName'] == 'maanviljelijä'


class TestSubPipelineCreation:

    def should_build_subpipeline_correctly_and_extract_data_using_given_configuration(self):
        pipeline = build_pipeline_from_yaml('pipeline_creation/tests/subpipeline_config.yaml')
        results = pipeline.process(test_data)

        assert results[0]['farmDetails']['farmTotalArea'] == 15.5
        assert results[0]['farmDetails']['animalHusbandry'] is True

    def should_build_pipelines_of_arbitrary_depth(self):
        pipeline = build_pipeline_from_yaml('pipeline_creation/tests/deep_subpipeline_config.yaml')
        results, metadata = pipeline.process(test_data)

        assert results['outerExtractor']['message'] == 'Level 1'
        assert results['outerExtractor']['innerExtractor']['message'] == 'Level 2'
        assert results['outerExtractor']['innerExtractor']['innerExtractor']['message'] == 'Level 3'

    @pytest.mark.skip()
    def should_produce_metadata_from_all_pipeline_levels(self):
        # TODO: We should add a working metadata building process for deep pipelines. Now
        # the metadata is not passed to upper pipelines correctly. This might require some rewrites for metadata collection
        pass


class OuterExtractor(BaseExtractor):
    extraction_key = 'outerExtractor'

    def __init__(self, cursor_location_depend_on=None, options=None, dependencies_contexts=None):
        super(OuterExtractor, self).__init__()
        self.message = options['message']

    def _extract(self, entry, extraction_results, extraction_metadata):
        results = {}
        if self._sub_extraction_pipeline:
            results, metadata = self._sub_extraction_pipeline.process({'text': entry['text']})
            results['message'] = self.message

        return self._add_to_extraction_results(results, extraction_results, extraction_metadata)


class SubExtractor(BaseExtractor):
    extraction_key = 'innerExtractor'

    def __init__(self, cursor_location_depend_on=None, options=None, dependencies_contexts=None):
        super(SubExtractor, self).__init__()
        self.message = options['message']

    def _extract(self, entry, extraction_results, extraction_metadata):
        results = {}
        if self._sub_extraction_pipeline:
            results, metadata = self._sub_extraction_pipeline.process({'text': entry['text']})

        results['message'] = self.message

        return self._add_to_extraction_results(results, extraction_results, extraction_metadata)
