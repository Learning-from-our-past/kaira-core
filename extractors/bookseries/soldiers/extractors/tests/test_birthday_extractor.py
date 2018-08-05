import pytest
from extractors.bookseries.soldiers.extractors.birthday_extractor import BirthdayExtractor


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
