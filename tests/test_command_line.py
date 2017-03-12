import pytest
from subprocess import run
import os
import shutil
import json

class TestCommandLineSmoke:
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

    @pytest.mark.only
    def should_process_small_farmers_xml_and_save_to_json(self):
        file_path = 'temp/json_export_tests/results.json'
        results = run(['python', 'main.py', '-i', 'tests/data/small_farmers_smoke_test.xml', '-o', file_path])

        assert results.returncode == 0

        with open(file_path, encoding='utf8') as data_file:
            result_data = json.load(data_file, encoding='utf8')

        assert len(result_data) == 3

    @pytest.mark.only
    def should_process_great_farmers_xml_and_save_to_json(self):
        file_path = 'temp/json_export_tests/results.json'
        results = run(['python', 'main.py', '-i', 'tests/data/great_farmers_smoke_test.xml', '-o', file_path])

        assert results.returncode == 0

        with open(file_path, encoding='utf8') as data_file:
            result_data = json.load(data_file, encoding='utf8')

        assert len(result_data) == 3

    def should_error_if_unsupported_xml_is_read(self):
        file_path = 'temp/json_export_tests/results.json'
        results = run(['python', 'main.py', '-i', 'tests/data/unsupported_file_smoke_test.xml', '-o', file_path])

        assert results.returncode == 1