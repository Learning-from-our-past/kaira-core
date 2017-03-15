import pytest
from book_extractors.farmers.extraction.extractors.childextractor import ChildExtractor
from book_extractors.farmers.tests.extraction.children.mock_person_data import EXPECTED_CHILDREN, CHILDREN_TEXTS


class TestChildrenExtraction:

    @pytest.yield_fixture(autouse=True)
    def child_extractor(self):
        return ChildExtractor(None, None)

    @pytest.mark.skip
    def should_extract_twins_correctly(self):
        # Cases like in TWINS_AND_EXTRA_INFO_CHILDREN
        # TODO: Needs extra logic. Maybe good case for BNF parser?
        pass

    @pytest.mark.skip
    def should_ignore_extra_information_between_children(self):
        # Cases like in TWINS_AND_EXTRA_INFO_CHILDREN
        # TODO: Needs extra logic. Maybe good case for BNF parser?
        pass

    def should_extract_children_correctly(self, child_extractor):
        children = child_extractor.extract({'text': CHILDREN_TEXTS[0]}, {'data': {}, 'cursor_locations': {}})['data']['children']

        assert len(children) == 3
        assert children[0] == EXPECTED_CHILDREN[0]
        assert children[1] == EXPECTED_CHILDREN[1]
        assert children[2] == EXPECTED_CHILDREN[2]


