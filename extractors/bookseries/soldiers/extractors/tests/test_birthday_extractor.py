import pytest
from extractors.bookseries.soldiers.extractors.birthday_extractor import (
    BirthdayExtractor,
)


class TestSoldierBirthdayExtraction:
    @pytest.yield_fixture(autouse=True)
    def birthday_extractor(self, th):
        return th.setup_extractor(BirthdayExtractor(None, {'remove_spaces': False}))

    def should_extract_date_in_normal_format(self, birthday_extractor):
        text = 'Testinen, Viljami testeri, s 12,3.05 Paimi'
        results, metadata = birthday_extractor.extract({'text': text}, {}, {})

        assert results['birthday']['birthDay'] == 12
        assert results['birthday']['birthMonth'] == 3
        assert results['birthday']['birthYear'] == 1905

    def should_extract_date_with_month_in_written_format(self, birthday_extractor):
        text = 'Testinen, Viljami testeri, s marrask 13 Lahti'
        results, metadata = birthday_extractor.extract({'text': text}, {}, {})

        assert results['birthday']['birthDay'] is None
        assert results['birthday']['birthMonth'] == 11
        assert results['birthday']['birthYear'] == 1913

    def should_not_extract_date_which_comes_after_pso_keyword(self, birthday_extractor):
        text = 'Testinen, Viljami testeri, mv. Pso vsta 42 Vaimo Vaimonen, s 10.2.18 Savitaipale'
        results, metadata = birthday_extractor.extract({'text': text}, {}, {})

        assert results['birthday']['birthDay'] is None
        assert results['birthday']['birthMonth'] is None
        assert results['birthday']['birthYear'] is None

    def should_not_extract_date_which_comes_after_pso_keyword_ignoring_case(
        self, birthday_extractor
    ):
        text = 'Testinen, Viljami testeri, mv. pso vsta 42 Vaimo Vaimonen, s 10.2.18 Savitaipale'
        results, metadata = birthday_extractor.extract({'text': text}, {}, {})

        assert results['birthday']['birthDay'] is None
        assert results['birthday']['birthMonth'] is None
        assert results['birthday']['birthYear'] is None
