import pytest
from book_extractors.karelians.extraction.extractors.farm_extractor import FarmDetailsExtractor


class TestFarmExtraction:
    @pytest.yield_fixture(autouse=True)
    def farm_extractor(self):
        return FarmDetailsExtractor(None, None)

    def verify_flags(self, expected_flags_and_texts, flag, farm_extractor):
        for e in expected_flags_and_texts:
            results, metadata = farm_extractor.extract({'text': e[0]}, {}, {})
            assert results['farmDetails'][flag] is e[1]

    def verify_farm_details_were_found(self, expected, farm_extractor):
        for e in expected:
            results, metadata = farm_extractor.extract({'text': e[0]}, {}, {})
            assert (results['farmDetails'] is not None) is e[1]

    def should_mark_animal_husbandry_true_if_it_is_mentioned_in_text(self, farm_extractor):
        self.verify_flags([
            ('Maanviljelyksen ohella Testikkäät harjoittavat karjanhoitoa.', True),
            ('Maanviljelyksen ohella Testikkäät harjoittavat karjataloutta.', True),
            ('Testikkäiden tila on karjatalous.', True)
        ], 'animalHusbandry', farm_extractor)

    def should_return_none_if_no_farm_properties_were_found(self, farm_extractor):
        self.verify_farm_details_were_found([
            ('Testikkäillä on traktori.', False),
            ('Emäntä Testikäs on käynyt karjatalouskoulun.', False),
            ('Isäntä Testikäs on karjanhoitaja.', False)
        ], farm_extractor)

    def should_mark_dairy_farm_true_if_it_is_mentioned_in_text_in_relevant_meaning(self, farm_extractor):
        self.verify_flags([
            ('Maanviljelyksen ohella Testikkäillä on lypsykarjaa.', True),
            ('Maanviljelyksen ohella Testikkäillä on lypsy- ja lihakarjaa.', True),
            ('Emäntä on voittanut lypsykilpailun. Karjanhoitoa harjoitetaan.', False),
            ('Tilalla on siirrytty lypsykarjasta teuraskarjaan. Karjanhoitoa harjoitetaan.', False),
        ], 'dairyFarm', farm_extractor)

