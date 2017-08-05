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
        result, metadata = owner_extractor.extract({'text': owner_text}, {}, {})
        data = result['ownerDetails']

        assert data['firstNames'] == 'Uuno'
        assert data['surname'] == 'Säämäki'
        assert data['ownerFrom'] is None
        assert data['gender'] == 'Male'
