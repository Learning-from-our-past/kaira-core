import pytest
from extractors.bookseries.karelians.extractors.child_extractor import ChildExtractor
from extractors.bookseries.karelians.extractors.tests.children.mock_person_data import (
    CHILDREN_TEXTS,
    EXPECTED,
)


class TestChildrenExtraction:
    @pytest.yield_fixture(autouse=True)
    def child_extractor(self, th):
        return th.setup_extractor(ChildExtractor(None, None))

    def should_extract_children_correctly_when_string_ends_to_syntyneet_word_and_fill_birth_location_accordingly(
        self, child_extractor, th
    ):
        result, metadata = child_extractor.extract(
            {'text': CHILDREN_TEXTS['common_birth_place']}, {}, {}
        )
        children = result['children']

        th.omit_property(children, 'latitude')
        th.omit_property(children, 'longitude')
        assert len(children) == 3
        assert children[0] == EXPECTED['common_birth_place'][0]
        assert children[1] == EXPECTED['common_birth_place'][1]
        assert children[2] == EXPECTED['common_birth_place'][2]

    def should_fill_birth_place_data_correctly_when_each_kid_has_different_birth_place(
        self, child_extractor, th
    ):
        result, metadata = child_extractor.extract(
            {'text': CHILDREN_TEXTS['different_birth_places']}, {}, {}
        )

        children = result['children']
        th.omit_property(children, 'latitude')
        th.omit_property(children, 'longitude')

        assert len(children) == 2
        assert children[0] == EXPECTED['different_birth_places'][0]
        assert children[1] == EXPECTED['different_birth_places'][1]
