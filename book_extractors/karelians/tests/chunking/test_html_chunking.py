import pytest
import os
import shutil
from lxml import etree
from book_extractors.karelians.chunktextfile import PersonPreprocessor
from book_extractors.karelians.tests.chunking import mock_html_data
from book_extractors.karelians.tests.chunking import expected_xml_data


class TestHtmlChunking:
    @pytest.fixture(autouse=True)
    def person_preprocessor(self):
        return PersonPreprocessor('siirtokarjalaiset')

    @pytest.fixture()
    def image_test_paths(self):
        test_path = 'temp/testikarjalaiset'
        mock_img_path = 'temp/test_image/test_img.jpg'
        img_dir_path = os.path.split(mock_img_path)[0]
        if not os.path.exists(img_dir_path):
            os.makedirs(img_dir_path)
        mock_img = open(mock_img_path, 'w', encoding='utf-8')
        mock_img.close()
        test_deletion_path = '{}_images'.format(test_path)

        if os.path.exists(test_deletion_path):
            shutil.rmtree(test_deletion_path)

        yield mock_img_path, test_path

        if os.path.exists(test_deletion_path):
            shutil.rmtree(test_deletion_path)
        if os.path.exists(img_dir_path):
            shutil.rmtree(img_dir_path)

    def should_correctly_chunk_typical_html_into_xml_person_entries(self, person_preprocessor):
        persons = person_preprocessor.chunk_text(mock_html_data.TWO_PEOPLE, 'testikarjalaiset', 1)
        assert etree.tostring(persons, pretty_print=True, encoding='unicode') == expected_xml_data.TWO_PEOPLE

    def should_correctly_chunk_people_whose_entries_start_inside_another_persons_entry(self, person_preprocessor):
        persons = person_preprocessor.chunk_text(mock_html_data.MID_ENTRY_PEOPLE, 'testikarjalaiset', 1)
        assert etree.tostring(persons, pretty_print=True, encoding='unicode') == expected_xml_data.MID_ENTRY_PEOPLE

    def should_correctly_identify_page_number_and_tag_person_entries_with_it(self, person_preprocessor):
        persons = person_preprocessor.chunk_text(mock_html_data.ENTRIES_ACROSS_PAGES, 'testikarjalaiset', 1)
        assert etree.tostring(persons, pretty_print=True, encoding='unicode') == expected_xml_data.ENTRIES_ACROSS_PAGES

    def should_not_chunk_people_with_lowercase_names(self, person_preprocessor):
        persons = person_preprocessor.chunk_text(mock_html_data.LOWER_CASE_NAME, 'testikarjalaiset', 1)
        assert etree.tostring(persons, pretty_print=True, encoding='unicode') == expected_xml_data.NO_RESULT

    def should_not_consider_military_units_to_be_people_whose_entries_start_within_other_peoples_entries(self, person_preprocessor):
        persons = person_preprocessor.chunk_text(mock_html_data.MILITARY_UNIT_IN_ENTRY, 'testikarjalaiset', 1)
        assert etree.tostring(persons, pretty_print=True, encoding='unicode') == expected_xml_data.MILITARY_UNIT_IN_ENTRY

    def should_correctly_create_path_for_image_and_copy_image_with_correct_caption(self, person_preprocessor, image_test_paths):
        img_path, test_path = image_test_paths
        caption = 'Salainen Nainen'
        img_test_html = r'<img src={} style="width:82pt;height:104pt;"/>\n<p>{}</p>'.format(img_path, caption)
        data_for_test = mock_html_data.HTML_CONTAINER.format(img_test_html)
        persons = person_preprocessor.chunk_text(data_for_test, test_path, 1)

        assert os.path.isfile('{}_images/{}.jpg'.format(test_path, caption.replace(' ', ''))) is True
