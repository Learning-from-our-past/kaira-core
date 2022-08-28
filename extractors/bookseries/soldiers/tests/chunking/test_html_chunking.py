import pytest
import xml.etree.ElementTree as ET
from extractors.bookseries.soldiers.chunktextfile import PersonPreprocessor
from extractors.bookseries.soldiers.tests.chunking import mock_html_data
from extractors.bookseries.soldiers.tests.chunking import expected_xml_data


class TestSoldiersHtmlChunking:
    @pytest.fixture(autouse=True)
    def person_preprocessor(self):
        return PersonPreprocessor('suomenrintamamiehet')

    def should_correctly_chunk_typical_html_into_xml_person_entries(
        self, person_preprocessor
    ):
        persons = person_preprocessor.chunk_text(
            mock_html_data.TWO_PEOPLE, 'rintamamiehet', 1
        )
        assert persons == expected_xml_data.TWO_PEOPLE

    def should_correctly_identify_page_number_and_tag_person_entries_with_it(
        self, person_preprocessor
    ):
        persons = person_preprocessor.chunk_text(
            mock_html_data.ENTRIES_ACROSS_PAGES, 'rintamamiehet', 1
        )

        document_root = ET.fromstring(persons)
        assert document_root[0].attrib['approximated_page'] == '140-142'
        assert document_root[1].attrib['approximated_page'] == '141-143'
