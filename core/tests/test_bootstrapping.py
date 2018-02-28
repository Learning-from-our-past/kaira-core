import pytest
from lxml import etree
import core.bootstrap as bootstrapper


def should_find_available_manifest_files_from_directory():
    available_bookseries = bootstrapper.find_available_bookseries_from_directory('core/tests/mock_data/manifest_mock_directories')
    assert len(available_bookseries) == 2


class TestBookseriesSetup:

    def should_setup_bookseries_for_supported_bookseries(self):
        bookseries = bootstrapper.setup_extraction_framework_for_bookseries('siirtokarjalaiset',
                                                                            'core/tests/mock_data/manifest_mock_directories',
                                                                            None)
        assert bookseries is not None
        assert bookseries._manifest['book_series_id'] == 'siirtokarjalaiset'

    def should_raise_error_if_given_book_series_is_not_supported(self):
        with pytest.raises(bootstrapper.BookSeriesNotSupportedException):
            bootstrapper.setup_extraction_framework_for_bookseries('suomen-cs-pelaajat',
                                                                   'core/tests/mock_data/manifest_mock_directories',
                                                                   None)


class TestBookSeries:

    @pytest.fixture()
    def xml_document(self):
        xml_parser = etree.XMLParser(encoding="utf8")
        return etree.parse('./core/tests/mock_data/datafile1.xml', parser=xml_parser).getroot()

    @pytest.fixture()
    def bookseries(self, xml_document):
        bookseries_id = xml_document.attrib['bookseries']
        return bootstrapper.setup_extraction_framework_for_bookseries(bookseries_id,
                                                                      'core/tests/mock_data/manifest_mock_directories',
                                                                      None)

    def should_convert_xml_entries_to_dict_objects(self, bookseries, xml_document):
        person_entry_dicts = bookseries._xml_to_extractor_format(xml_document)

        assert len(person_entry_dicts) == 1
        assert person_entry_dicts[0] == {
            'text': 'lorem ipsum dolor',
            'full_text': 'lorem ipsum dolor',
            'name': 'TESTINEN, TESTI',
            'approximated_page': '0-2',
            'img_path': 'images/testinenImage.jpg'
        }
