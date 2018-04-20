import pytest
from extractors.bookseries.soldiers.extractors.name_extractor import NameExtractor


class TestSoldierNameExtraction:

    @pytest.yield_fixture(autouse=True)
    def name_extractor(self, th):
        return th.setup_extractor(NameExtractor(None, None))

    def should_extract_firstname_and_lastname(self, name_extractor):
        text = 'TESTINEN, Aapo, s 14.12.12 Sysmä, mv. Pso vsta 46 Hanna Vaimokas s 17 Savitaipale, emäntä.'
        results, metadata = name_extractor.extract({'text': text}, {}, {})

        assert results['name']['firstNames'] == 'Aapo'
        assert results['name']['lastName'] == 'TESTINEN'

    def should_extract_multiple_firstnames(self, name_extractor):
        text = 'TESTINEN, Aapo Ahti-Arto, s 14.12.12 Sysmä, mv. Pso vsta 46 Hanna Vaimokas s 17 Savitaipale, emäntä.'
        results, metadata = name_extractor.extract({'text': text}, {}, {})

        assert results['name']['firstNames'] == 'Aapo Ahti-Arto'

    def should_extract_lastname_with_hyphens(self, name_extractor):
        text = 'TESTINEN-TESTAAJA, Aapo, s 14.12.12 Sysmä, mv. Pso vsta 46 Hanna Vaimokas s 17 Savitaipale, emäntä.'
        results, metadata = name_extractor.extract({'text': text}, {}, {})

        assert results['name']['lastName'] == 'TESTINEN-TESTAAJA'

    def should_extract_names_from_slightly_varying_strings(self, name_extractor):
        texts = (
            ('AALTONEN, Jussi Testimies s 1.5.16 Tku', 'AALTONEN', 'Jussi Testimies'),
            ('AALTONEN. Hessu Hopo s 1.5.16 Tku', 'AALTONEN', 'Hessu Hopo'),
            ('ELOMAA (Kilkkilä), Aku Ankka, s 8.5.07 Nastola, mv.', 'ELOMAA', 'Aku Ankka'),
            ('KANT OLA, Mikki Hiiri, s 4.6.22 T re,', 'KANTOLA', 'Mikki Hiiri'),
            ('RAJANTIE ROSEHORN, Roope Ankka, s 14.7.18 Miehikkälä,', 'RAJANTIEROSEHORN', 'Roope Ankka'),
            ('TESTINEN, Kaarlo (Kalle) Markus, s 14.7.18 Miehikkälä,', 'TESTINEN', 'Kaarlo (Kalle) Markus')
        )

        for text, last_name, first_name in texts:
            results, metadata = name_extractor.extract({'text': text}, {}, {})
            assert results['name']['firstNames'] == first_name
            assert results['name']['lastName'] == last_name
