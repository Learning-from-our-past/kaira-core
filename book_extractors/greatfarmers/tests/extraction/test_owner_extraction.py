import pytest
from book_extractors.greatfarmers.extraction.extractors.owner_extractor import OwnerExtractor
from shared.gender_extract import Gender


class TestOwnerExtraction:

    @pytest.yield_fixture(autouse=True)
    def owner_extractor(self):
        Gender.load_names()
        return OwnerExtractor(None, None)

    def should_extract_owner_correctly_from_short_entry(self, owner_extractor):
        owner_text = "om Uuno Säämäki. Tila sijaitsee Testilän kylässä. Kokonaispinta-ala on 186,17 ha."
        result = owner_extractor.extract({'text': owner_text}, {})['ownerDetails']['results']

        assert result['firstNames'] == 'Uuno'
        assert result['surname'] == 'Säämäki'
        assert result['ownerFrom'] is None
        assert result['gender'] == 'Male'
