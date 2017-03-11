import pytest
from book_extractors.karelians.extraction.extractors.childextractor import ChildExtractor
from book_extractors.karelians.tests.extraction.children.mock_person_data import CHILDREN_TEXTS, EXPECTED


class TestChildrenExtraction:

    @pytest.yield_fixture(autouse=True)
    def child_extractor(self):
        return ChildExtractor(None)

    def should_extract_children_correctly_when_string_ends_to_syntyneet_word_and_fill_birth_location_accordingly(self, child_extractor):
        children = child_extractor.extract({'text': CHILDREN_TEXTS[0]})['children']

        assert len(children) == 3
        assert children[0] == EXPECTED[0]
        assert children[1] == EXPECTED[1]
        assert children[2] == EXPECTED[2]
