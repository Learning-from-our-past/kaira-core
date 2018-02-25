import pytest
from utils.gender_extract import Gender

class TestOwnerExtraction:

    @pytest.yield_fixture(autouse=True)
    def owner_extractor(self, th):
        Gender.load_names()
        return th.build_pipeline_from_yaml(OWNER_EXTRACTOR_CONFIG)

    def should_extract_owner_correctly_from_short_entry(self, owner_extractor):
        owner_text = "om Uuno Säämäki. Tila sijaitsee Testilän kylässä. Kokonaispinta-ala on 186,17 ha."
        result, metadata = owner_extractor.process({'text': owner_text})
        data = result['ownerDetails']

        assert data['firstNames'] == 'Uuno'
        assert data['surname'] == 'Säämäki'
        assert data['ownerFrom'] is None
        assert data['gender'] == 'Male'


OWNER_EXTRACTOR_CONFIG = """
pipeline:
  - !Extractor {
      module: "book_extractors.greatfarmers.extractors.owner_extractor",
      class_name: "OwnerExtractor",
      pipeline: [
        !Extractor {
            module: "book_extractors.greatfarmers.extractors.birthday_extractor",
            class_name: "BirthdayExtractor"
        }
      ]
    }
"""
