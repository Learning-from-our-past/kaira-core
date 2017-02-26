import pytest
import shutil
import os
import json
from books.farmers.resultjsonbuilder import ResultJsonBuilder
from books.farmers.tests.data_export.mock_person_data import PERSON_DATA, EXPECTED_JSON

class TestPersonPopulate:
    @pytest.yield_fixture(autouse=True)
    def json_test_dir(self):
        path = './temp/json_export_tests'
        if not os.path.exists(path):
            os.makedirs(path)
        yield path

        if os.path.exists(path):
            shutil.rmtree(path)

    def should_export_json_data_in_correct_format(self, json_test_dir):
        json_export = ResultJsonBuilder()
        file_path = os.path.join(json_test_dir, 'test.json')
        json_export.openJson(file_path)

        json_export.writeEntry(PERSON_DATA)
        json_export.closeJson()

        expected_data = json.loads(EXPECTED_JSON)

        with open(file_path, encoding='utf8') as data_file:
            result_data = json.load(data_file)

        assert len(result_data) == 1
        assert result_data == expected_data


