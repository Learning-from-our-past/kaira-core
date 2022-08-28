import pytest
from lxml import etree
from os import path
import core.bootstrap as bootstrapper


def should_find_available_manifest_files_from_directory():
    available_bookseries = bootstrapper.find_available_bookseries_from_directory(
        'core/tests/mock_data/manifest_mock_directories'
    )
    assert len(available_bookseries) == 3


class TestBookseriesSetup:
    def should_setup_bookseries_for_supported_bookseries(self):
        bookseries = bootstrapper.setup_extraction_framework_for_bookseries(
            'siirtokarjalaiset', 'core/tests/mock_data/manifest_mock_directories', None
        )
        assert bookseries is not None
        assert bookseries._manifest['book_series_id'] == 'siirtokarjalaiset'

    def should_raise_error_if_given_book_series_is_not_supported(self):
        with pytest.raises(bootstrapper.BookSeriesNotSupportedException):
            bootstrapper.setup_extraction_framework_for_bookseries(
                'suomen-cs-pelaajat',
                'core/tests/mock_data/manifest_mock_directories',
                None,
            )


class TestBookSeries:
    def _get_xml_document(self, filename):
        xml_parser = etree.XMLParser(encoding='utf8')
        file_path = path.join('./core/tests/mock_data/', filename)
        return etree.parse(file_path, parser=xml_parser).getroot()

    def _get_bookseries(self, xml_doc):
        bookseries_id = xml_doc.attrib['bookseries']
        return bootstrapper.setup_extraction_framework_for_bookseries(
            bookseries_id, 'core/tests/mock_data/manifest_mock_directories', None
        )

    def should_convert_xml_entry_to_dict_object(self):
        xml_document = self._get_xml_document('datafile1.xml')
        bookseries = self._get_bookseries(xml_document)
        person_entry_dict = bookseries.convert_xml_to_dict(xml_document[0])

        assert person_entry_dict == {
            'text': 'lorem ipsum dolor',
            'full_text': 'lorem ipsum dolor',
            'name': 'TESTINEN, TESTI',
            'approximated_page': '0-2',
            'img_path': 'images/testinenImage.jpg',
        }

    def should_convert_xml_entry_to_dict_object_when_bookseries_has_custom_converter(
        self,
    ):
        xml_document = self._get_xml_document('datafile2.xml')
        bookseries = self._get_bookseries(xml_document)
        person_entry_dict = bookseries.convert_xml_to_dict(xml_document[0])

        assert person_entry_dict == {
            'text': 'lorem ipsum dolor',
            'full_text': 'lorem ipsum dolor',
            'other': 'The eigenstates of a measurement are not disturbed by the observation.',
            'name': 'TESTINEN, TESTI',
            'approximated_page': '0-2',
            'img_path': 'images/testinenImage.jpg',
        }
