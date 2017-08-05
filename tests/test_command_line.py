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
            assert result_data[0]['kairaId'] == 'siirtokarjalaiset_1_3P'
            assert result_data[0]['spouse']['kairaId'] == 'siirtokarjalaiset_1_1S'
            assert result_data[1]['kairaId'] == 'siirtokarjalaiset_1_5P'
            assert result_data[1]['spouse']['kairaId'] == 'siirtokarjalaiset_1_4S'
            assert result_data[2]['kairaId'] == 'siirtokarjalaiset_1_10P'
            assert result_data[2]['spouse']['kairaId'] == 'siirtokarjalaiset_1_6S'

        def should_return_correct_birthlocation_without_control_characters(self):
            # FIXME: Move this test to some kind of preprocessor class when relevant implementation code is moved from
            # ExtractionPipeline to elsewhere
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/encoding_test.xml', '-o', file_path])

            assert results.returncode == 0

            with open(file_path, encoding='utf8') as data_file:
                result_data = json.load(data_file, encoding='utf8')

            assert result_data[0]['birthLocation']['locationName'] == 'Kuolemajärvi'

        def should_process_small_farmers_xml_and_save_to_json(self):
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/small_farmers_smoke_test.xml', '-o', file_path])

            assert results.returncode == 0

            with open(file_path, encoding='utf8') as data_file:
                result_data = json.load(data_file, encoding='utf8')

            assert len(result_data) == 3

            # Check that each entry has unique id
            assert result_data[0]['kairaId'] == 'pienviljelijat_1_2P'
            assert result_data[1]['kairaId'] == 'pienviljelijat_1_3P'
            assert result_data[2]['kairaId'] == 'pienviljelijat_1_9P'

        def should_process_great_farmers_xml_and_save_to_json(self):
            file_path = 'temp/json_export_tests/results.json'
            results = run(['python', 'main.py', '-i', 'tests/data/great_farmers_smoke_test.xml', '-o', file_path])

            assert results.returncode == 0

            with open(file_path, encoding='utf8') as data_file:
                result_data = json.load(data_file, encoding='utf8')

            assert len(result_data) == 3

            # Check that each person has unique id
            assert result_data[0]['kairaId']['results'] == 'suuretmaatilat_1_2P'
            assert result_data[0]['spouse']['results']['kairaId'] == 'suuretmaatilat_1_1S'
            assert result_data[1]['kairaId']['results'] == 'suuretmaatilat_1_4P'
            assert result_data[1]['spouse']['results']['kairaId'] == 'suuretmaatilat_1_3S'
            assert result_data[2]['kairaId']['results'] == 'suuretmaatilat_1_7P'
            assert result_data[2]['spouse']['results']['kairaId'] == 'suuretmaatilat_1_5S'

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
            xml_parser = etree.XMLParser(encoding="utf8")
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()
            book_series = xml_document.attrib["bookseries"]
            book_number = xml_document.attrib["book_number"]

            assert book_series == 'siirtokarjalaiset'
            assert book_number == '1'
            assert len(xml_document) == 2  # FIXME: There is a bug here. Does not produce last person. This should be 3.

        def should_convert_great_farmers_html_to_xml(self):
            file_path = 'temp/xml_export_tests/results.xml'
            results = run(
                ['python', 'main.py', '-c', 'tests/data/greatfarmers_convert_smoke_test.html', '-o', file_path, '-b',
                 'suuretmaatilat', '-n', '1'])

            assert results.returncode == 0
            xml_parser = etree.XMLParser(encoding="utf8")
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()
            book_series = xml_document.attrib["bookseries"]
            book_number = xml_document.attrib["book_number"]

            assert book_series == 'suuretmaatilat'
            assert book_number == '1'
            assert len(xml_document) == 2

        def should_convert_small_farmers_html_to_xml(self):
            file_path = 'temp/xml_export_tests/results.xml'
            results = run(
                ['python', 'main.py', '-c', 'tests/data/smallfarmers_convert_smoke_test.html', '-o', file_path, '-b',
                 'pienviljelijat', '-n', '1'])

            assert results.returncode == 0
            xml_parser = etree.XMLParser(encoding="utf8")
            xml_document = etree.parse(file_path, parser=xml_parser).getroot()
            book_series = xml_document.attrib["bookseries"]
            book_number = xml_document.attrib["book_number"]

            assert book_series == 'pienviljelijat'
            assert book_number == '1'
            assert len(xml_document) == 2
