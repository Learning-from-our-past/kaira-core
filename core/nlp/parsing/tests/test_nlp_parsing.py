import pytest
import os
import shutil
import xml.etree.ElementTree as ElementTree
from core.nlp.parsing.transform_xml import run_xml_data_transformation
from core import bootstrap


class TestNLPParsing:
    @pytest.fixture(autouse=True, scope='session')
    def nlp_test_dir(self):
        path = './temp/nlp_tests'
        if not os.path.exists(path):
            os.makedirs(path)
        yield path

        if os.path.exists(path):
            shutil.rmtree(path)

    @pytest.fixture(autouse=True, scope='session')
    def bookseries(self):
        return bootstrap.setup_extraction_framework_for_bookseries('siirtokarjalaiset',
                                                                   'extractors/bookseries/',
                                                                   None)

    @pytest.fixture(autouse=True, scope='session')
    def raw_test_data(self):
        path = 'core/nlp/parsing/tests/data/raw_test_data.xml'
        with open(path, mode='r', encoding='utf8') as xml_file:
            yield ElementTree.parse(xml_file)

    @pytest.fixture(autouse=True, scope='session')
    def transformed_test_data(self, bookseries, nlp_test_dir, raw_test_data):
        output_path = '{}/raw_test_data'.format(nlp_test_dir)
        preprocessed_path = run_xml_data_transformation(bookseries, raw_test_data, output_path)
        return preprocessed_path

    class TestTextPreprocessing:
        def should_preprocess_xml_file_and_output_text_file(self, transformed_test_data):
            assert os.path.isfile(transformed_test_data)

        def should_separate_person_entries_in_preprocessed_file_with_comments(self, transformed_test_data):
            with open(transformed_test_data, mode='r', encoding='utf8') as file:
                file_contents = file.read()

            entries = tuple(x for x in file_contents.split('###C: ') if x)
            assert len(entries) == 2
