import pytest
import os
import shutil
import xml.etree.ElementTree as ElementTree
from core.nlp.parsing.transform_xml import run_xml_data_transformation
from core import bootstrap
from collections import Counter
from core.nlp.parsing.parse_with_fdp import parse_through_fdp_and_output_file
from core.nlp.parsing.join_nlp_data_to_xml import add_conllu_data_to_xml


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

    @pytest.fixture(autouse=True, scope='session')
    def nlp_test_data(self, nlp_test_dir, transformed_test_data):
        output_path = '{}/raw_test_data'.format(nlp_test_dir)
        nlp_data_path = parse_through_fdp_and_output_file(transformed_test_data, output_path)
        return nlp_data_path

    @pytest.fixture(autouse=True, scope='session', name='raw_and_nlp_xml')
    def xml_with_raw_and_nlp_test_data(self, nlp_test_dir, raw_test_data, nlp_test_data):
        output_path = '{}/raw_and_nlp_test_data.xml'.format(nlp_test_dir)
        with open(output_path, mode='w', encoding='utf8') as output_file:
            nlp_and_raw_xml_path = add_conllu_data_to_xml(raw_test_data, nlp_test_data, output_file)
        return nlp_and_raw_xml_path

    class TestTextPreprocessing:
        @pytest.mark.skip()
        def should_preprocess_xml_file_and_output_text_file(self, transformed_test_data):
            assert os.path.isfile(transformed_test_data)

        @pytest.mark.skip()
        def should_separate_person_entries_in_preprocessed_file_with_comments(self, transformed_test_data):
            with open(transformed_test_data, mode='r', encoding='utf8') as file:
                file_contents = file.read()

            entries = tuple(x for x in file_contents.split('###C: ') if x)
            assert len(entries) == 2

    class TestNLPDataGeneration:
        @pytest.mark.skip()
        def should_process_preprocessed_data_with_fdp_and_output_file(self, nlp_test_data):
            assert os.path.isfile(nlp_test_data)

        @pytest.mark.skip()
        def should_have_person_entries_separated_by_comments_in_nlp_data_file(self, nlp_test_data):
            with open(nlp_test_data, mode='r', encoding='utf8') as file:
                file_contents = file.read()

            entries = tuple(x for x in file_contents.split('###C: ') if x)
            assert len(entries) == 2

    class TestNLPDataJoiningToXML:
        @pytest.mark.skip()
        def should_join_nlp_data_to_xml_and_output_file(self, raw_and_nlp_xml):
            assert os.path.isfile(raw_and_nlp_xml)

        @pytest.mark.skip()
        def should_have_person_elements_with_raw_and_conllu_subelements_in_xml_file(self, raw_and_nlp_xml):
            xml_doc = ElementTree.parse(raw_and_nlp_xml)
            root = xml_doc.getroot()
            c = Counter()
            assert len(root) == 2
            for child in root:
                elem1, elem2 = child
                c.update([elem1.tag, elem2.tag])
            assert c['CONLLU'] == 2
            assert c['RAW'] == 2
