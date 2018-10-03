import pytest
from subprocess import run
import os
import shutil
import json
from lxml import etree


class TestCommandLineSmoke:
    class TestExtraction:
        @pytest.yield_fixture(autouse=True)
        def json_test_dir(self):
            path = './temp/json_export_tests'
            if not os.path.exists(path):
                os.makedirs(path)
            yield path

            if os.path.exists(path):
                shutil.rmtree(path)

        def should_process_karelian_xml_and_save_to_json(self):
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/karelian_smoke_test.xml', '-o', file_path])

            assert results.returncode == 0

            with open(file_path, encoding='utf8') as data_file:
                result_data = json.load(data_file, encoding='utf8')

            assert len(result_data) == 3

            # Check that each person has unique id
            assert result_data[0]['primaryPerson']['kairaId'] == 'siirtokarjalaiset_1_1P'
            assert result_data[0]['spouse']['kairaId'] == 'siirtokarjalaiset_1_1S_1'
            assert result_data[1]['primaryPerson']['kairaId'] == 'siirtokarjalaiset_1_2P'
            assert result_data[1]['spouse']['kairaId'] == 'siirtokarjalaiset_1_2S_1'
            assert result_data[2]['primaryPerson']['kairaId'] == 'siirtokarjalaiset_1_3P'
            assert result_data[2]['spouse']['kairaId'] == 'siirtokarjalaiset_1_3S_1'

        def should_return_correct_birthlocation_without_control_characters(self):
            # FIXME: Move this test to some kind of preprocessor class when relevant implementation code is moved from
            # ExtractionPipeline to elsewhere
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/encoding_test.xml', '-o', file_path])

            assert results.returncode == 0

            with open(file_path, encoding='utf8') as data_file:
                result_data = json.load(data_file, encoding='utf8')

            assert result_data[0]['primaryPerson']['birthLocation']['locationName'] == 'Kuolemajärvi'

        def should_process_small_farmers_xml_and_save_to_json(self):
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/small_farmers_smoke_test.xml', '-o', file_path])

            assert results.returncode == 0

            with open(file_path, encoding='utf8') as data_file:
                result_data = json.load(data_file, encoding='utf8')

            assert len(result_data) == 3

            # Check that each entry has unique id
            assert result_data[0]['kairaId'] == 'pienviljelijat_1_1P'
            assert result_data[1]['kairaId'] == 'pienviljelijat_1_2P'
            assert result_data[2]['kairaId'] == 'pienviljelijat_1_3P'

        def should_process_great_farmers_xml_and_save_to_json(self):
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/great_farmers_smoke_test.xml', '-o', file_path])

            assert results.returncode == 0

            with open(file_path, encoding='utf8') as data_file:
                result_data = json.load(data_file, encoding='utf8')

            assert len(result_data) == 3

            # Check that each person has unique id
            assert result_data[0]['kairaId'] == 'suuretmaatilat_1_1P'
            assert result_data[0]['spouse']['kairaId'] == 'suuretmaatilat_1_1S_1'
            assert result_data[1]['kairaId'] == 'suuretmaatilat_1_2P'
            assert result_data[1]['spouse']['kairaId'] == 'suuretmaatilat_1_2S_1'
            assert result_data[2]['kairaId'] == 'suuretmaatilat_1_3P'
            assert result_data[2]['spouse']['kairaId'] == 'suuretmaatilat_1_3S_1'

        def should_error_if_unsupported_xml_is_read(self):
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/unsupported_file_smoke_test.xml', '-o', file_path])

            assert results.returncode == 1

    class TestHtmlToXmlConversion:
        @pytest.yield_fixture(autouse=True)
        def xml_test_dir(self):
            path = './temp/xml_export_tests'
            if not os.path.exists(path):
                os.makedirs(path)
            yield path

            if os.path.exists(path):
                shutil.rmtree(path)

        def should_convert_karelian_html_to_xml(self):
            file_path = 'temp/xml_export_tests/results.xml'
            results = run(['python', 'main.py', '-c', 'tests/data/karelian_convert_smoke_test.html', '-o', file_path, '-b', 'siirtokarjalaiset', '-n', '1'])

            assert results.returncode == 0
            xml_parser = etree.XMLParser(encoding='utf8')
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()
            book_series = xml_document.attrib['bookseries']
            book_number = xml_document.attrib['book_number']

            assert book_series == 'siirtokarjalaiset'
            assert book_number == '1'
            assert len(xml_document) == 4

        def should_convert_karelian_html_to_xml_and_delete_duplicates(self):
            file_path = 'temp/xml_export_tests/results_no_duplicates.xml'
            results = run([
                'python', 'main.py', '-c', 'tests/data/karelian_convert_smoke_test.html',
                '-o', file_path, '-b', 'siirtokarjalaiset', '-n', '1', '--filter'
            ])

            assert results.returncode == 0
            xml_parser = etree.XMLParser(encoding='utf8')
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()
            book_series = xml_document.attrib['bookseries']
            book_number = xml_document.attrib['book_number']

            assert book_series == 'siirtokarjalaiset'
            assert book_number == '1'
            assert len(xml_document) == 3

        def should_convert_great_farmers_html_to_xml(self):
            file_path = 'temp/xml_export_tests/results.xml'
            results = run(
                ['python', 'main.py', '-c', 'tests/data/greatfarmers_convert_smoke_test.html', '-o', file_path, '-b',
                 'suuretmaatilat', '-n', '1'])

            assert results.returncode == 0
            xml_parser = etree.XMLParser(encoding='utf8')
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()
            book_series = xml_document.attrib['bookseries']
            book_number = xml_document.attrib['book_number']

            assert book_series == 'suuretmaatilat'
            assert book_number == '1'
            assert len(xml_document) == 2

        def should_convert_small_farmers_html_to_xml(self):
            file_path = 'temp/xml_export_tests/results.xml'
            results = run(
                ['python', 'main.py', '-c', 'tests/data/smallfarmers_convert_smoke_test.html', '-o', file_path, '-b',
                 'pienviljelijat', '-n', '1'])

            assert results.returncode == 0
            xml_parser = etree.XMLParser(encoding='utf8')
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()
            book_series = xml_document.attrib['bookseries']
            book_number = xml_document.attrib['book_number']

            assert book_series == 'pienviljelijat'
            assert book_number == '1'
            assert len(xml_document) == 2

    class TestNLPTagging:
        @pytest.yield_fixture(autouse=True)
        def xml_test_dir(self):
            path = './temp/nlp_tagging_tests'
            if not os.path.exists(path):
                os.makedirs(path)
            yield path

            if os.path.exists(path):
                shutil.rmtree(path)

        def should_tag_karelian_xml_with_conllu(self):
            file_path = 'temp/nlp_tagging_tests/results.xml'
            results = run(['python', 'main.py', '-t', 'tests/data/karelian_nlp_smoke_test.xml', '-o', file_path])

            assert results.returncode == 0
            xml_parser = etree.XMLParser(encoding='utf8')
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()

            conllu_lengths = [len(conllu.text) for raw, conllu in xml_document]
            # Each time this test is run on CI, nlp-setup is run as well. If the NLP people of
            # University of Turku have retrained their machine learning models (which are
            # downloaded as part of nlp-setup), the lengths of these strings may be slightly
            # than before, so we can't check for exact lengths.
            assert all(length > 3000 for length in conllu_lengths)
