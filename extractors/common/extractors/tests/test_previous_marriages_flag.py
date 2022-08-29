import pytest
from extractors.common.extractors.previous_marriages_flag_extractor import (
    PreviousMarriagesFlagExtractor,
)


class TestPreviousMarriagesFlag:
    @pytest.yield_fixture(autouse=True)
    def extractor(self, th):
        return th.setup_extractor(PreviousMarriagesFlagExtractor(None, None))

    def should_return_true_if_text_contains_mentions_of_previous_marriages(
        self, extractor
    ):
        entry = {
            'text': 'maanviljelijä, synt. 15. 10. 99 Kurkijoella. Puol. Vaimo o.s. Vaimoke, emäntä, '
            'synt. 23. 12. -06 Kurkijoella. Lapset: Lapsi -25, Lapsikaks -28. Molemmat ovat syntyneet '
            'Kurkijoella ja ovat miehen ensimmäisestä avioliitosta.'
        }
        extraction_results = {}
        results, metadata = extractor.extract(entry, extraction_results, {})
        assert results['previousMarriagesFlag'] is True

        entry = {
            'text': '0. s. Testaaja, ent. Testeri. synt 22. 2. 20 Viipurissa. Puol. Mies Miehekäs, maanviljelijä, '
            'synt.1.    2. -16 Alavudella. Avioit. -47. Lapset: Tyttö 38 Viipuri. Tyttö -40'
            ' Jyväskylä. Lapset rouvan aikaisemmasta avioliitosta. Asuinp Karjalassa: Viipuri.'
        }
        extraction_results = {}
        results, metadata = extractor.extract(entry, extraction_results, {})
        assert results['previousMarriagesFlag'] is True

    def should_return_false_if_text_does_not_mention_previous_marriages(
        self, extractor
    ):
        entry = {
            'text': 'työmies, synt. 19. 6. -01 Pyhäjärvellä. Puol. Vaimo o.s. Testaaja. rouva, synt. 21 4 -06 '
            'Rau dussa. Avioit. -29. Lapset: Tyttö -29, Poika -31, Poika -32, Poika -35, Tyttö -38. '
            'Syntyneet Pyhäjärvellä, Poika -41 Alavus. Asuinp, Karjalassa.'
        }

        extraction_results = {}
        results, metadata = extractor.extract(entry, extraction_results, {})
        assert results['previousMarriagesFlag'] is False
