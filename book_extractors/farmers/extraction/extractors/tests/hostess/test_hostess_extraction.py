import pytest
from book_extractors.farmers.extraction.extractors.tests.hostess.mock_person_data import HOSTESS_TEXTS, EXPECTED


class TestHostessExtraction:
    @pytest.yield_fixture(autouse=True)
    def hostess_extractor(self, th):
        return th.build_pipeline_from_yaml(HOSTESS_EXTRACTOR_CONFIG)

    def should_extract_hostess_correctly(self, hostess_extractor):
        result, metadata = hostess_extractor.process({'text': HOSTESS_TEXTS['normal']})
        hostess = result['hostess']
        assert hostess == EXPECTED[0]

    def should_return_none_if_hostess_is_not_found(self, hostess_extractor):
        result, metadata = hostess_extractor.process({'text': HOSTESS_TEXTS['no_hostess']})
        hostess = result['hostess']

        assert hostess == EXPECTED[1]
        assert metadata['hostess']['errors'] == {'hostessNotFound': 4}


HOSTESS_EXTRACTOR_CONFIG = """
pipeline:
  - !Extractor {
      module: "book_extractors.farmers.extraction.extractors.hostess_extractor",
      class_name: "HostessExtractor",
      pipeline: [
        !Extractor {
            module: "book_extractors.farmers.extraction.extractors.birthday_extractor",
            class_name: "BirthdayExtractor"
        }
      ]
    }
"""
