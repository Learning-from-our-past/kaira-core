import pytest
from extractors.bookseries.karelians.extractors.location_extractor import (
    BirthdayLocationExtractor,
)
from extractors.bookseries.karelians.extractors.birthday_extractor import (
    BirthdayExtractor,
)


class TestBirthDayLocation:
    @pytest.yield_fixture(autouse=True)
    def location_extractor(self, th):
        return th.setup_extractor(BirthdayLocationExtractor(BirthdayExtractor, None))

    def should_extract_birth_location_and_fill_in_region_and_coordinates_from_geo_db(
        self, location_extractor
    ):
        # Simulate the stopping location of the previous extractor which gives this extractor the 'anchor point' to
        # begin the extraction.
        previous_metadata = {BirthdayExtractor.extraction_key: {'cursorLocation': 16}}

        result, metadata = location_extractor.extract(
            {'text': 'synt. 10. 8. -17 Sippola. Avioit. -38.'}, {}, previous_metadata
        )

        assert result['birthLocation']['locationName'] == 'Sippola'
        assert result['birthLocation']['region'] == 'other'
        assert result['birthLocation']['latitude'] is not None
        assert result['birthLocation']['longitude'] is not None

    def should_extract_birth_location_but_leave_region_and_coordinates_empty_if_they_were_not_found(
        self, location_extractor
    ):
        previous_metadata = {BirthdayExtractor.extraction_key: {'cursorLocation': 16}}

        result, metadata = location_extractor.extract(
            {'text': 'synt. 10. 8. -17 Räävinpyrstö. Avioit. -38.'},
            {},
            previous_metadata,
        )

        assert result['birthLocation']['locationName'] == 'Räävinpyrstö'
        assert result['birthLocation']['region'] is None
        assert result['birthLocation']['latitude'] is None
        assert result['birthLocation']['longitude'] is None


class TestBirthDayExtractor:
    @pytest.yield_fixture(autouse=True)
    def mock_entries(self):
        return [
            {
                'text': 'maanviljelijä, synt. 22. 9. -09Hiitolassa. Puol. Vaimo Vaimoikas o.s.',
                'result': '2291909',
            },
            {
                'text': 'Testikäinen, emäntä, synt. 30. 8. -21 Hiitolassa. Avioit. -44. Poika: ',
                'result': '3081921',
            },
            {
                'text': 'o.s. Testinen, rouva, synt. 29. 9. -18 Hiitolassa. Puol. ',
                'result': '2991918',
            },
            {
                'text': 'Testimies, ahtaaja, synt. 12. 2.    16Ahlaisissa. Avioit. -44. Lapset: ',
                'result': '1221916',
            },
            {
                'text': 'o.s. Testeri, vanhaemäntä. synt. 14, 3. -84 Kuolemajärvellä. Puol. ',
                'result': '1431884',
            },
            {
                'text': 'Testaaja, synt. Muurilassa. Kuoli. -41 Urjalassa Lapset:',
                'result': 'NoneNoneNone',
            },
            {
                'text': 'o.s. Laadunvalvoja. ent. Koodari, emäntä, synt. 1. 2. -92 Uudellakirkolla. Puol. ',
                'result': '121892',
            },
            {
                'text': 'Testaaja, maanviljelijä, synt. -91 Uudellakirkolla. Kuoli. -63 Halikossa. Lapset: ',
                'result': 'NoneNone1891',
            },
        ]

    def should_extract_dates_correctly(self, mock_entries, th):
        birthday_extractor = th.setup_extractor(BirthdayExtractor(None, None))

        for test_text in mock_entries:
            result, metadata = birthday_extractor.extract(test_text, {}, {})
            assert (
                '{}{}{}'.format(
                    result['birthData']['birthDay'],
                    result['birthData']['birthMonth'],
                    result['birthData']['birthYear'],
                )
                == test_text['result']
            )
