import pytest
from pipeline_creation.yaml_parser import parse_config, build_pipeline_from_yaml
from book_extractors.karelians.extraction.extractors.name_extractor import NameExtractor

def should_load_yaml():
    result = parse_config('pipeline_creation/tests/test_config.yaml')
    assert result['book_series'] == 'Siirtokarjalaisten tie'
    assert len(result['pipeline']) == 4
    assert type(result['pipeline'][0]) is NameExtractor


def should_build_and_run_pipeline():
    pipeline = build_pipeline_from_yaml('pipeline_creation/tests/test_config.yaml')

    test_data = {
        'name': 'TESTINEN. VÄINÖ',
        'text': 'maanviljelijä, synt. 26. 1. -27 Testilässä. Puol. Vaimo Vaimonen o.s. Vaimoke, emäntä, synt. 7 7. -32 '
                'Enossa. Avioit. -51. Lapset: Martti Olavi An tero -51, Martta Lyyli 53, Mikko Timo Tapani -55, Matti '
                'Armas Juhani -57. Merja Riitta Sinikka -59, Marjatta Raija Orvokki -63. Syntyneet Enossa Asuinp. '
                'Karjalassa: Ruskeala, Kaalamo 27—40, 40—44 Muut asuinp.: Svsmä, Rapola -40 Isokyrö. Lehmijoki 41—45, '
                'Kiihtelysvaara 45—48, Eno, Haapalahti 48—. Testiset asuvat maatilalla, jonka pinta-ala on 15,5 ha, '
                'viljeltyä on 5.7 ha. Maanviljelyksen ohella harjoitetaan karjanhoitoa.'
    }

    results = pipeline.process(test_data)

    assert results[0]['name']['surname'] == 'TESTINEN'
    assert results[0]['profession']['professionName'] == 'maanviljelijä'
