import pytest
from book_extractors.farmers.extraction.extractors.hostessextractor import HostessExtractor
from book_extractors.farmers.tests.extraction.hostess.mock_person_data import HOSTESS_TEXTS, EXPECTED


class TestHostessExtraction:
    @pytest.yield_fixture(autouse=True)
    def hostess_extractor(self):
        return HostessExtractor(None)

    def should_extract_hostess_correctly(self, hostess_extractor):
        hostess = hostess_extractor.extract({'text': HOSTESS_TEXTS['normal']})['hostess']
        del hostess['birthData']['cursorLocation']
        assert hostess == EXPECTED[0]

    def should_return_none_if_hostess_is_not_found(self, hostess_extractor):
        hostess = hostess_extractor.extract({'text': HOSTESS_TEXTS['no_hostess']})['hostess']
        assert hostess == EXPECTED[1]